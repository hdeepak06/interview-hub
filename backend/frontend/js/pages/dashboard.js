/**
 * DEEPAK INTERVIEW HUB — Student Dashboard Controller
 * Fetches real activity data from the backend API.
 * Never displays hardcoded placeholder stats; renders informative empty states for new learners.
 */

'use strict';

document.addEventListener('DOMContentLoaded', async () => {
  // Check auth
  if (!APIClient.getToken()) {
    window.location.href = '/pages/login.html';
    return;
  }

  const loader = document.getElementById('dashboard-loader');
  const content = document.getElementById('dashboard-content');

  try {
    const data = await APIClient.get('/dashboard/');
    renderDashboard(data);
  } catch (err) {
    console.warn('Dashboard fetch fallback (offline/new setup):', err);
    // Provide a safe zeroed state for newly created accounts before backend connects
    renderDashboard({
      questions_attempted: 0,
      accuracy_percentage: 0,
      mock_tests_completed: 0,
      learning_streak_days: 0,
      subjects_progress: [],
      recent_activities: [],
      difficulty_distribution: {
        easy: 0,
        medium: 0,
        difficult: 0
      }
    });
  } finally {
    if (loader) loader.style.display = 'none';
    if (content) content.style.display = 'block';
  }

  function renderDashboard(data) {
    // Top stats
    document.getElementById('stat-attempted').textContent = data.questions_attempted ?? 0;
    document.getElementById('stat-accuracy').textContent = `${Math.round(data.accuracy_percentage ?? 0)}%`;
    document.getElementById('stat-mock-tests').textContent = data.mock_tests_completed ?? 0;
    document.getElementById('stat-streak').textContent = `${data.learning_streak_days ?? 0} Days`;

    // Difficulty breakdown
    const easyCount = data.difficulty_distribution?.easy ?? 0;
    const medCount = data.difficulty_distribution?.medium ?? 0;
    const diffCount = data.difficulty_distribution?.difficult ?? 0;

    document.getElementById('diff-easy-count').textContent = `${easyCount} Solved`;
    document.getElementById('diff-medium-count').textContent = `${medCount} Solved`;
    document.getElementById('diff-difficult-count').textContent = `${diffCount} Solved`;

    const totalSolved = (easyCount + medCount + diffCount) || 1;
    document.getElementById('diff-easy-bar').style.width = `${(easyCount / totalSolved) * 100}%`;
    document.getElementById('diff-medium-bar').style.width = `${(medCount / totalSolved) * 100}%`;
    document.getElementById('diff-difficult-bar').style.width = `${(diffCount / totalSolved) * 100}%`;

    // Subject Mastery
    const subjectList = document.getElementById('subject-progress-list');
    if (subjectList) {
      if (!data.subjects_progress || data.subjects_progress.length === 0) {
        subjectList.innerHTML = `
          <div class="empty-state py-8">
            <div class="empty-state-icon" style="width: 3rem; height: 3rem; font-size: 1.5rem;">📚</div>
            <div class="empty-state-title" style="font-size: 1rem;">No subject practice yet</div>
            <p class="empty-state-description" style="font-size: 0.8rem; margin-bottom: 1rem;">
              Start answering technical questions or solving exercises to track your mastery.
            </p>
            <a href="/pages/subjects.html" class="btn btn-primary btn-sm">Explore Subjects</a>
          </div>
        `;
      } else {
        subjectList.innerHTML = data.subjects_progress.map(sub => `
          <div>
            <div class="flex items-center justify-between text-sm mb-1">
              <span class="font-medium text-white">${sub.name}</span>
              <span class="text-xs text-gold-400">${sub.solved_count}/${sub.total_count} (${sub.percentage}%)</span>
            </div>
            <div class="progress-bar">
              <div class="progress-bar-fill" style="width: ${sub.percentage}%;"></div>
            </div>
          </div>
        `).join('');
      }
    }

    // Recent Activity
    const activityList = document.getElementById('recent-activity-list');
    if (activityList) {
      if (!data.recent_activities || data.recent_activities.length === 0) {
        activityList.innerHTML = `
          <div class="empty-state py-8">
            <div class="empty-state-icon" style="width: 3rem; height: 3rem; font-size: 1.5rem;">⚡</div>
            <div class="empty-state-title" style="font-size: 1rem;">No recent activities</div>
            <p class="empty-state-description" style="font-size: 0.8rem; margin-bottom: 1rem;">
              Your practice questions, mock test attempts, and coding submissions will be recorded here.
            </p>
            <a href="/pages/questions.html" class="btn btn-secondary btn-sm">Start Question Bank</a>
          </div>
        `;
      } else {
        activityList.innerHTML = data.recent_activities.map(act => `
          <div class="flex items-center justify-between p-3 rounded bg-navy-700 text-sm">
            <div>
              <div class="font-medium text-white">${act.title}</div>
              <div class="text-xs text-gray-400">${act.timestamp}</div>
            </div>
            <span class="badge ${act.status === 'correct' ? 'badge-easy' : 'badge-difficult'}">
              ${act.status}
            </span>
          </div>
        `).join('');
      }
    }
  }
});

