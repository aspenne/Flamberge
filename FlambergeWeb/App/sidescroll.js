function transformScroll(event) {
    // Adjust the scrolling speed by multiplying with a factor (e.g., 3)
    var speedFactor = 0.4;
  
    // Find the section under the mouse cursor
    var sectionUnderCursor = findSectionUnderCursor(event);
  
    // Adjust the element and scrolling behavior based on the section under the cursor
    if (sectionUnderCursor) {
      event.preventDefault(); // Prevent default scrolling behavior
      sectionUnderCursor.scrollLeft += (event.deltaY + event.deltaX) * speedFactor;
    }
  }
  
  function findSectionUnderCursor(event) {
    // Get all film sections
    var filmSections = document.querySelectorAll('.film-section');
  
    // Find the section that is under the mouse cursor
    var sectionUnderCursor = null;
  
    filmSections.forEach(function (section) {
      var boundingBox = section.getBoundingClientRect();
  
      // Check if the mouse coordinates are within the bounding box of the section
      if (
        event.clientX >= boundingBox.left &&
        event.clientX <= boundingBox.right &&
        event.clientY >= boundingBox.top &&
        event.clientY <= boundingBox.bottom
      ) {
        sectionUnderCursor = section;
      }
    });
  
    return sectionUnderCursor;
  }
  
  var element = document.scrollingElement || document.documentElement;
  element.addEventListener('wheel', transformScroll, { passive: false });
  