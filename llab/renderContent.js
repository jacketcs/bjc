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
   <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#${id}" aria-expanded=${isVisible} aria-controls="${id}">
   <strong>${optionalContent[contentType]}</strong>
  </button>
  <div id='${id}' class='collapse'>
    ${this.innerHTML}
  </div>`;
  // Use class "ifTime show" to show by default.
  // BS3 uses the 'in' class to show content, TODO: update this for v5.
  if (isVisible) {
    $(`#${id}`).addClass('in');
    $(this).removeClass('show');
  }
});


snapRunURLBase = "https://snap.berkeley.edu/snap/snap.html#open:";
snapRunURLBaseVersion = "https://snap.berkeley.edu/versions/VERSION/snap.html#open:";
rootURL = "/"

// returns the current domain with a cors proxy if needed

// TODO: Support for a CORS proxy has been removed.
// If we have a reliable enough CORS proxy, we can consider re-adding it.
// It is expected that you host llab content in an environment where CORS is allowed.
getSnapRunURL = function(targeturl, options) {
    if (!targeturl) { return ''; }

    if (targeturl.indexOf('http') == 0 || targeturl.indexOf('//') == 0) {
        // pointing to some non-local resource... do nothing!!
        return targeturl;
    }

    // internal resource!
    var finalurl = snapRunURLBase;
    if (options && options.version) {
        finalurl = snapRunURLBaseVersion.replace('VERSION', options.version);
    }

    var currdom = "https://camp.echa.ng";
    if (currdom == "localhost") {
        currdom = 'http://' + currdom + ":" + window.location.port;
        // finalurl = finalurl.replace('https://snap', 'http://extensions.snap');
    }
    finalurl = finalurl + currdom + targeturl;

    return finalurl;
};

$('a.run').each(function(_i) {
    $(this).attr('target', '_blank');
    $(this).attr('href', getSnapRunURL(this.getAttribute('href')));
});

$('.js-run').each(function(_i) {
    $(this).attr('target', '_blank');
    $(this).attr('href', getSnapRunURL(this.getAttribute('href'))); // {version: 'v7'}
});
