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

// Image preview
fileInput.addEventListener('change', function() {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
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
  resultCard.style.display = 'none';
  loader.style.display = 'none';
  resetBtn.style.display = 'none';
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('dragover');
});
uploadArea.addEventListener('dragleave', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
});
uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    fileInput.dispatchEvent(new Event('change'));
  }
});

// Loader animation
function showLoader(show) {
  loader.style.display = show ? 'block' : 'none';
}

// Confetti animation
function showConfetti() {
  confettiDiv.innerHTML = '';
  for (let i = 0; i < 30; i++) {
    const conf = document.createElement('div');
    conf.className = 'confetti';
    conf.style.left = Math.random() * 100 + '%';
    conf.style.animationDelay = (Math.random() * 0.7) + 's';
    confettiDiv.appendChild(conf);
  }
  setTimeout(() => confettiDiv.innerHTML = '', 2000);
}

// AJAX form submit
form.addEventListener('submit', function(e) {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) return;
  showLoader(true);
  resultCard.style.display = 'none';
  resetBtn.style.display = 'none';
  const formData = new FormData();
  formData.append('file', file);
  fetch('/predict', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      showLoader(false);
      if (data.label) {
        unicodeLabel.textContent = data.label;
        resultCard.style.display = 'block';
        resetBtn.style.display = 'inline-block';
        addToHistory(preview.src, data.label);
        showConfetti();
      } else if (data.error) {
        unicodeLabel.textContent = 'Error: ' + data.error;
        resultCard.style.display = 'block';
      } else {
        unicodeLabel.textContent = 'Unknown error.';
        resultCard.style.display = 'block';
      }
    })
    .catch(err => {
      showLoader(false);
      unicodeLabel.textContent = 'Error: ' + err;
      resultCard.style.display = 'block';
    });
});

// Copy to clipboard
copyBtn.addEventListener('click', function() {
  const text = unicodeLabel.textContent;
  navigator.clipboard.writeText(text);
  copyBtn.textContent = '✅';
  setTimeout(() => copyBtn.textContent = '📋', 1200);
});

// Reset
resetBtn.addEventListener('click', function() {
  fileInput.value = '';
  preview.src = '#';
  preview.style.display = 'none';
  resultCard.style.display = 'none';
  resetBtn.style.display = 'none';
  submitBtn.style.display = 'none';
});

// Prediction history
function addToHistory(imgSrc, unicode) {
  history.unshift({ imgSrc, unicode });
  if (history.length > 10) history.pop();
  renderHistory();
}
function renderHistory() {
  historyList.innerHTML = '';
  history.forEach(item => {
    const li = document.createElement('li');
    const thumb = document.createElement('img');
    thumb.src = item.imgSrc;
    thumb.alt = 'Thumbnail';
    thumb.style.width = '32px';
    thumb.style.height = '32px';
    thumb.style.borderRadius = '6px';
    thumb.style.marginRight = '8px';
    li.appendChild(thumb);
    const code = document.createElement('span');
    code.textContent = item.unicode;
    li.appendChild(code);
    historyList.appendChild(li);
  });
}

// Add pop-in animation for preview
const style = document.createElement('style');
style.innerHTML = `.pop-in { animation: popIn 0.5s; } @keyframes popIn { 0% { transform: scale(0.8); opacity: 0.5; } 100% { transform: scale(1); opacity: 1; } } .confetti { position: absolute; top: 0; width: 12px; height: 12px; border-radius: 50%; background: hsl(${Math.random()*360},90%,60%); opacity: 0.8; animation: confettiDrop 1.2s linear forwards; } @keyframes confettiDrop { 0% { top: 0; opacity: 1; } 100% { top: 100px; opacity: 0; } }`;
document.head.appendChild(style); 