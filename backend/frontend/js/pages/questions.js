/**
 * DEEPAK INTERVIEW HUB — Question Bank Controller
 * Dynamic filtering, keyword search, accordion toggle for solutions/explanations,
 * and bookmark interactions.
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('filter-search');
  const subjectSelect = document.getElementById('filter-subject');
  const difficultySelect = document.getElementById('filter-difficulty');
  const listEl = document.getElementById('questions-list');
  const loaderEl = document.getElementById('questions-loader');
  const emptyEl = document.getElementById('questions-empty');
  const paginationEl = document.getElementById('questions-pagination');

  let currentPage = 1;
  let debounceTimer = null;

  // Initialize filters from URL search params
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('subject')) subjectSelect.value = urlParams.get('subject');
  if (urlParams.get('difficulty')) difficultySelect.value = urlParams.get('difficulty');
  if (urlParams.get('q')) searchInput.value = urlParams.get('q');

  async function fetchQuestions(page = 1) {
    currentPage = page;
    loaderEl.style.display = 'block';
    listEl.style.display = 'none';
    emptyEl.style.display = 'none';
    paginationEl.style.display = 'none';

    const params = new URLSearchParams();
    params.set('page', page);
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim());
    if (subjectSelect.value) params.set('subject', subjectSelect.value);
    if (difficultySelect.value) params.set('difficulty', difficultySelect.value);

    try {
      const response = await APIClient.get(`/questions/?${params.toString()}`);
      renderQuestions(response);
    } catch (err) {
      console.warn('API error or server offline, rendering fallback sample:', err);
      // If backend is not yet populated, show empty state or fallback
      emptyEl.style.display = 'flex';
    } finally {
      loaderEl.style.display = 'none';
    }
  }

  function renderQuestions(data) {
    const results = data.results || (Array.isArray(data) ? data : []);

    if (results.length === 0) {
      emptyEl.style.display = 'flex';
      return;
    }

    listEl.innerHTML = results.map((q, idx) => {
      const diffClass = `difficulty-${(q.difficulty || 'easy').toLowerCase()}`;
      const badgeClass = `badge-${(q.difficulty || 'easy').toLowerCase()}`;

      return `
        <div class="card card-question ${diffClass} p-6" data-id="${q.id}">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span class="badge ${badgeClass}">${q.difficulty}</span>
              <span class="badge badge-subject">${q.subject_name || q.subject || 'General'}</span>
              ${q.topic_name ? `<span class="tag">${q.topic_name}</span>` : ''}
            </div>
            <button class="btn btn-ghost btn-sm btn-bookmark" data-id="${q.id}" title="Bookmark Question">
              ${q.is_bookmarked ? '🔖 Saved' : '🔖 Save'}
            </button>
          </div>

          <h3 class="text-lg font-bold text-white mb-3">
            ${q.question_text}
          </h3>

          <!-- Options if MCQ -->
          ${q.options && q.options.length ? `
            <div class="preview-options mb-4">
              ${q.options.map(opt => `
                <div class="preview-option">
                  <strong>${opt.option_label})</strong> ${opt.option_text}
                </div>
              `).join('')}
            </div>
          ` : ''}

          <!-- Accordion Toggle for Explanation -->
          <div class="accordion-item">
            <button class="btn btn-secondary btn-sm question-toggle-btn">
              <span>View Answer &amp; Explanation</span>
              <span class="accordion-arrow">&darr;</span>
            </button>

            <div class="question-solution mt-4 p-4 rounded bg-navy-950 border border-subtle" style="display: none;">
              <div class="mb-3">
                <span class="text-xs uppercase font-bold text-easy">Correct Answer:</span>
                <div class="text-white font-medium mt-1">${q.correct_answer}</div>
              </div>

              ${q.explanation ? `
                <div class="mb-3">
                  <span class="text-xs uppercase font-bold text-gold-400">Detailed Explanation:</span>
                  <div class="text-sm text-gray-300 mt-1 leading-relaxed">${q.explanation}</div>
                </div>
              ` : ''}

              ${q.code_example ? `
                <div class="code-block my-3">
                  <div class="code-block-header">
                    <span class="code-language">Reference Code</span>
                  </div>
                  <pre><code>${escapeHtml(q.code_example)}</code></pre>
                </div>
              ` : ''}

              ${q.expected_output ? `
                <div class="mb-3">
                  <span class="text-xs uppercase font-bold text-gray-400">Expected Output:</span>
                  <pre class="code-inline block p-2 mt-1">${escapeHtml(q.expected_output)}</pre>
                </div>
              ` : ''}

              ${q.interview_tip ? `
                <div class="alert alert-info mt-3 mb-0">
                  <span class="alert-icon">💡</span>
                  <div class="alert-content">
                    <div class="alert-title">Interview Tip</div>
                    <div class="alert-message">${q.interview_tip}</div>
                  </div>
                </div>
              ` : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');

    listEl.style.display = 'flex';

    // Attach solution toggle listeners
    listEl.querySelectorAll('.question-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const solution = btn.parentElement.querySelector('.question-solution');
        const isHidden = solution.style.display === 'none';
        solution.style.display = isHidden ? 'block' : 'none';
        btn.querySelector('span:first-child').textContent = isHidden ? 'Hide Solution' : 'View Answer & Explanation';
      });
    });

    // Attach bookmark listeners
    listEl.querySelectorAll('.btn-bookmark').forEach(btn => {
      btn.addEventListener('click', async () => {
        const qId = btn.getAttribute('data-id');
        if (!APIClient.getToken()) {
          Toast.warning('Please log in to save bookmarks');
          return;
        }
        try {
          await APIClient.post('/bookmarks/', { question: qId });
          btn.textContent = '🔖 Saved';
          Toast.success('Question saved to bookmarks!');
        } catch (err) {
          Toast.error(err.message || 'Failed to update bookmark');
        }
      });
    });

    // Render pagination
    if (data.total_pages && data.total_pages > 1) {
      renderPagination(data.total_pages, currentPage);
    }
  }

  function renderPagination(totalPages, page) {
    paginationEl.innerHTML = '';
    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement('button');
      btn.className = `pagination-btn ${i === page ? 'is-active' : ''}`;
      btn.textContent = i;
      btn.addEventListener('click', () => fetchQuestions(i));
      paginationEl.appendChild(btn);
    }
    paginationEl.style.display = 'flex';
  }

  function escapeHtml(text) {
    if (!text) return '';
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Filter Event Listeners
  subjectSelect.addEventListener('change', () => fetchQuestions(1));
  difficultySelect.addEventListener('change', () => fetchQuestions(1));

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchQuestions(1);
    }, 350);
  });

  // Initial load
  fetchQuestions(1);
});

