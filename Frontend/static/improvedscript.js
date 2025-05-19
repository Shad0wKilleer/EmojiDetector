const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const previewWrapper = document.getElementById('preview-wrapper');
const uploadArea = document.getElementById('upload-area');
const form = document.getElementById('upload-form');
const resultCard = document.getElementById('result-card');
const unicodeLabel = document.getElementById('unicode-label');
const copyBtn = document.getElementById('copy-btn');
const loader = document.getElementById('loader');
const resetBtn = document.getElementById('reset-btn');
const historyList = document.getElementById('history-list');
const confettiDiv = document.getElementById('confetti');
const submitBtn = document.getElementById('submit-btn');

let history = [];

// ⬆️ Image preview handler
fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = 'block';
      previewWrapper.classList.add('pop-in');
      setTimeout(() => previewWrapper.classList.remove('pop-in'), 500);
      submitBtn.style.display = 'inline-block';
    };
    reader.readAsDataURL(file);
  } else {
    preview.style.display = 'none';
    submitBtn.style.display = 'none';
  }
  resetState();
});

// 🖱️ Drag-and-drop support
['dragover', 'dragleave', 'drop'].forEach(event =>
  uploadArea.addEventListener(event, (e) => {
    e.preventDefault();
    uploadArea.classList.toggle('dragover', event === 'dragover');
  })
);

uploadArea.addEventListener('drop', (e) => {
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    fileInput.dispatchEvent(new Event('change'));
  }
});

// 🌀 Show/hide loader
function showLoader(show) {
  loader.style.display = show ? 'block' : 'none';
}

// 🎊 Confetti celebration
function showConfetti() {
  confettiDiv.innerHTML = '';
  for (let i = 0; i < 30; i++) {
    const conf = document.createElement('div');
    conf.className = 'confetti';
    conf.style.left = `${Math.random() * 100}%`;
    conf.style.background = `hsl(${Math.random() * 360}, 90%, 60%)`;
    conf.style.animationDelay = `${Math.random() * 0.7}s`;
    confettiDiv.appendChild(conf);
  }
  setTimeout(() => confettiDiv.innerHTML = '', 2000);
}

// 📤 AJAX Form Submission
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) return;

  showLoader(true);
  resetState();

  const formData = new FormData();
  formData.append('file', file);

  fetch('/predict', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      showLoader(false);
      unicodeLabel.textContent = data.label || `Error: ${data.error || 'Unknown error'}`;
      resultCard.style.display = 'block';
      resetBtn.style.display = 'inline-block';

      if (data.label) {
        addToHistory(preview.src, data.label);
        showConfetti();
      }
    })
    .catch(err => {
      showLoader(false);
      unicodeLabel.textContent = `Error: ${err.message}`;
      resultCard.style.display = 'block';
    });
});

// 📋 Copy to clipboard
copyBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(unicodeLabel.textContent);
  copyBtn.textContent = '✅';
  setTimeout(() => copyBtn.textContent = '📋', 1200);
});

// 🔄 Reset interface
resetBtn.addEventListener('click', () => {
  fileInput.value = '';
  preview.src = '';
  preview.style.display = 'none';
  submitBtn.style.display = 'none';
  resetState();
});

function resetState() {
  resultCard.style.display = 'none';
  loader.style.display = 'none';
  resetBtn.style.display = 'none';
}

// 🧾 History rendering
function addToHistory(imgSrc, unicode) {
  history.unshift({ imgSrc, unicode });
  if (history.length > 10) history.pop();
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = '';
  history.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      <img src="${item.imgSrc}" alt="Thumb" style="width: 32px; height: 32px; border-radius: 6px;">
      <span>${item.unicode}</span>
    `;
    historyList.appendChild(li);
  });
}

// 📦 Add styling for animations
const style = document.createElement('style');
style.innerHTML = `
  .pop-in {
    animation: popIn 0.5s;
  }
  @keyframes popIn {
    0% { transform: scale(0.8); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
  }
  .confetti {
    position: absolute;
    top: 0;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    opacity: 0.8;
    animation: confettiDrop 1.2s linear forwards;
  }
  @keyframes confettiDrop {
    0% { top: 0; opacity: 1; }
    100% { top: 100px; opacity: 0; }
  }
`;
document.head.appendChild(style);
