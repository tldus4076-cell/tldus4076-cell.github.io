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
      content.hidden = true;
    });

    var target = document.getElementById(tabId);
    target.hidden = false;
    target.classList.add('active');
  });
});
