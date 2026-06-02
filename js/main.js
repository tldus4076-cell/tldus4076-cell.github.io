// ===== Game Server Study Hub - Main JS =====

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initTopicCards();
  initTabs();
  initQuizzes();
  initCopyButtons();
  initProgress();
});

// ===== Navbar =====
function initNav() {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.navbar nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
  }
  // Active link
  const path = window.location.pathname;
  document.querySelectorAll('.navbar nav a').forEach(a => {
    if (a.getAttribute('href') === path || (path === '/' && a.getAttribute('href') === '/')) {
      a.classList.add('active');
    }
  });
}

// ===== Topic Cards Accordion =====
function initTopicCards() {
  document.querySelectorAll('.topic-header').forEach(header => {
    header.addEventListener('click', () => {
      const card = header.closest('.topic-card');
      const wasOpen = card.classList.contains('open');
      // Close all
      document.querySelectorAll('.topic-card').forEach(c => c.classList.remove('open'));
      // Toggle clicked
      if (!wasOpen) {
        card.classList.add('open');
        // Update progress
        updateProgress(card.dataset.topic);
        // Smooth scroll
        setTimeout(() => {
          card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
      }
    });
  });
}

// ===== Tabs =====
function initTabs() {
  document.querySelectorAll('.tabs').forEach(tabGroup => {
    const buttons = tabGroup.querySelectorAll('.tab');
    const parent = tabGroup.parentElement;
    const contents = parent.querySelectorAll('.tab-content');
    
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const target = parent.querySelector(`#${btn.dataset.tab}`);
        if (target) target.classList.add('active');
      });
    });
  });
}

// ===== Quizzes =====
function initQuizzes() {
  document.querySelectorAll('.quiz-box').forEach(quiz => {
    const correct = quiz.dataset.answer;
    const options = quiz.querySelectorAll('.quiz-option');
    const result = quiz.querySelector('.quiz-result');
    let answered = false;

    options.forEach(opt => {
      opt.addEventListener('click', () => {
        if (answered) return;
        answered = true;

        if (opt.dataset.value === correct) {
          opt.classList.add('correct');
          result.textContent = '✅ 정답입니다! 잘하셨어요!';
          result.classList.add('correct-result');
        } else {
          opt.classList.add('wrong');
          // Show correct answer
          options.forEach(o => {
            if (o.dataset.value === correct) o.classList.add('correct');
          });
          result.textContent = '❌ 틀렸습니다. 정답은 위에서 초록색으로 표시됩니다.';
          result.classList.add('wrong-result');
        }
        result.classList.add('show');
      });
    });
  });
}

// ===== Copy Buttons =====
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.closest('.code-block').querySelector('code');
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = '복사됨!';
        setTimeout(() => btn.textContent = '복사', 1500);
      });
    });
  });
}

// ===== Progress Tracking =====
function initProgress() {
  if (!document.querySelector('.progress-container')) return;
  
  const saved = localStorage.getItem('studyProgress');
  if (saved) {
    const topics = JSON.parse(saved);
    topics.forEach(t => {
      const card = document.querySelector(`[data-topic="${t}"]`);
      if (card) card.dataset.visited = 'true';
    });
  }
  renderProgress();
}

function updateProgress(topic) {
  let topics = JSON.parse(localStorage.getItem('studyProgress') || '[]');
  if (!topics.includes(topic)) {
    topics.push(topic);
    localStorage.setItem('studyProgress', JSON.stringify(topics));
  }
  renderProgress();
}

function renderProgress() {
  const total = document.querySelectorAll('.topic-card[data-topic]').length;
  const visited = JSON.parse(localStorage.getItem('studyProgress') || '[]').length;
  const percent = total > 0 ? Math.round((visited / total) * 100) : 0;
  
  const fill = document.querySelector('.progress-fill');
  const text = document.querySelector('.progress-text');
  if (fill) fill.style.width = percent + '%';
  if (text) text.textContent = `학습 진도: ${visited}/${total} (${percent}%)`;
}

// ===== Typing Effect for Code =====
function typeCode(element, code, speed = 20) {
  let i = 0;
  element.textContent = '';
  function type() {
    if (i < code.length) {
      element.textContent += code[i];
      i++;
      setTimeout(type, speed);
    }
  }
  type();
}
