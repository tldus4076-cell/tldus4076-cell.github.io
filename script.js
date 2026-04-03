document.querySelectorAll('.quick-link').forEach(function(link) {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    var tabId = this.getAttribute('data-tab');

    document.querySelectorAll('.quick-link').forEach(function(l) {
      l.classList.remove('active');
    });
    this.classList.add('active');

    document.querySelectorAll('.tab-content').forEach(function(content) {
      content.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var firstTab = document.querySelector('.quick-link[data-tab="about"]');
  if (firstTab) {
    firstTab.click();
  }
});