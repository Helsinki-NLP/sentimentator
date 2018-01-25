
/* annotate.js
 * Hide and reveal user interface elements to create a nice UX flow.
 */

/* Toggle the visibility of the fine sentiment buttons
 */
function fineToggle(visibility) {
  var elem = document.querySelectorAll('#fine1, #fine2');
  Array.prototype.forEach.call(elem, function(e) {
    e.style.display = visibility;
  });
}

/* Reveal submit button
 */
function submitReveal() {
  document.getElementById('submit').style.display = 'block';
}

function init() {
  /* Query for different button elements
   */
  var posneg  = document.querySelectorAll('#pos, #neg');
  var neutral = document.querySelectorAll('#neut');
  var fine    = document.querySelectorAll('#fine1 input, #fine2 input');
  var hidden  = document.querySelectorAll('#fine1, #fine2, #submit');

  /* Attach onChange callback functions to each button
   */
  Array.prototype.forEach.call(posneg, function(e) {
    e.onchange = function() {
      fineToggle('block');
      submitReveal();
    }
  });
  Array.prototype.forEach.call(neutral, function(e) {
    e.onchange = function() {
      fineToggle('none');
      submitReveal();
    }
  });
  // Array.prototype.forEach.call(fine, function(e) {
  //   e.onchange = submitReveal;
  // });

  /* Hide fine sentiments and submit button
   */
  Array.prototype.forEach.call(hidden, function(e) {
    e.style.display = 'none';
  });
}

/* Wait for DOM to fully load before starting to tinker with it
 */
if (document.attachEvent? document.readyState === "complete": document.readyState !== "loading") {
  init();
} else {
  document.addEventListener('DOMContentLoaded', init);
}