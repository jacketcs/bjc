/** curriculum.js
*
*  sets up a curriculum page -- either local or external.
*
*  JavaScript Dependencies:
*   llab.js
*   jQuery
*   library.js
*/

llab.file = "";
llab.url_list = [];

var FULL = llab.selectors.FULL,
hamburger = llab.fragments.hamburger;

// Executed on each page load.
// TODO: Should probably be slip into a better place.
llab.secondarySetUp = function() {

  // fix snap links so they run snap
  $('a.run').each(function(_i) {
    $(this).attr('target', '_blank');
    $(this).attr('href', llab.getSnapRunURL(this.getAttribute('href')));
  });

  $('.js-run').each(function(_i) {
    $(this).attr('target', '_blank');
    $(this).attr('href', llab.getSnapRunURL(this.getAttribute('href'))); // {version: 'v7'}
  });

  const  optionalContent = {
    'ifTime': 'If There Is Time…',
    'takeItFurther': 'Take It Further…',
    'takeItTeased': 'Take It Further…',
  };

  // Return the name of the class on element if it is a class in optionalContent
  function lookupClassName(optionalContent, classList) {
    for (let key in optionalContent) {
      if (classList.includes(key)) {
        return key;
      }
    }
    return null;
  }

  let classSelector = `div.${Object.keys(optionalContent).join(',div.')}`;
  $(classSelector).each(function(i) {
    let classList = Array.from(this.classList);
    let isVisible = classList.indexOf('show') > -1;
    let contentType = lookupClassName(optionalContent, classList);
    let id = `hint-${contentType}-${i}`;
    this.innerHTML = `
    <button class="btn btn-link" type="button" data-bs-target="#${id}" data-bs-toggle='collapse'
      role="button" aria-controls="#${id}" aria-expanded=${isVisible}>
      <strong>${optionalContent[contentType]}</strong>
    </button>
    <div id='${id}' class='collapse'>
      ${this.innerHTML}
    </div>`;
    // Use class "if show" to show by default.
    // BS3 uses the 'in' class to show content, TODO: update this for v5.
    if (isVisible) {
      $(`#${id}`).addClass('in');
      $(this).removeClass('show');
    }
  });

}; // close secondarysetup();


/** A prelimary API for defining loading additional content based on triggers.
*  @{param} array TRIGGERS is an array of {trigger, callback} pairs.
*  a `trigger` is currently a CSS selector that gets passed to $ to see if any
*  of those elements are on the current page. If the elements are found then a
*  `callback` is called with no arguments.
*  TODO: Cleanup and test this code.
*  TODO: Explore ideas for better trigger options?
*/
llab.additionalSetup = function(triggers) {
  var items;
  triggers.forEach(function (obj) {
    if (obj.trigger && obj.function) {
      items = $(trigger);
      if (items.length) {
        Function.call(null, obj.function);
      }
    }
  });
}


// Create an iframe when loading from an empty curriculum page
// Used for embedded content. (Videos, books, etc)
llab.addFrame = function() {
  var source = llab.getQueryParameter("src");

  var frame = $(document.createElement("iframe")).attr(
    {'src': source, 'class': 'content-embed'}
  );

  var conent = $(document.createElement('div'));
  conent.append(
    '<a href=' + source + ' target="_blank">Open page in new window</a><br />'
  );
  conent.append(frame);

  $(FULL).append(conent);
};

// Pages directly within a lab. Excludes 'topic' and 'course' pages.
llab.isCurriculum = function() {
  if (llab.getQueryParameter('topic')) {
    return ![
      llab.empty_topic_page_path, llab.topic_launch_page, llab.alt_topic_page
    ].includes(location.pathname);
  }
  return false;
}


/* Return the index value of this page in reference to the lab.
* Indicies are 0 based, and this excludes query parameters because
* they could become re-ordered. */
llab.thisPageNum = function() {
  return llab.pageNum;
}

// Setup the nav and parse the topic file.
$(document).ready(function() {
  llab.secondarySetUp();
});
