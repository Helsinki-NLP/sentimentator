/* annotate.js
 * Hide and reveal user interface elements to create a nice UX flow.
 */

function fineReveal() {
  var elem = document.querySelectorAll('#fine1, #fine2');
  Array.prototype.forEach.call(elem, function(e) {
    e.style.display = 'block';
  });
}

function submitReveal() {
  document.getElementById('submit').style.display = 'block';
}

function init() {
  var coarse = document.querySelectorAll('#pos, #neg');
  var neutral = document.querySelectorAll('#neut');
  var fine   = document.querySelectorAll('#fine1 input, #fine2 input');
  var hidden = document.querySelectorAll('#fine1, #fine2, #submit');

  Array.prototype.forEach.call(coarse, function(e) {
    e.onchange = fineReveal;
  });
    Array.prototype.forEach.call(neutral, function(e) {
    e.onchange = submitReveal;
  });
  Array.prototype.forEach.call(fine, function(e) {
    e.onchange = submitReveal;
  });
  Array.prototype.forEach.call(hidden, function(e) {
    e.style.display = 'none';
  });
}

if (document.attachEvent? document.readyState === "complete": document.readyState !== "loading") {
  init();
} else {
  document.addEventListener('DOMContentLoaded', init);
}
