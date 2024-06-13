setInterval(changeLinks, 100)

const exclude = new RegExp("NEUTRON_EXCLUDE_REGEX_PATTERN")

function changeLinks() {
  // Get list of all links in the page
  var links = document.getElementsByTagName("a"); 
  // Loop through links
  for(var i=0,l=links.length; i<l; i++) {
     // No need to use `getAttribute`, href is defined getter in all browsers
     loc = links[i].href;
     if ((links[i].href.substring(0, 8) == "https://" || links[i].href.substring(0, 7 == "http://")) && !exclude.test(links[i].href)){
        links[i].href = "open:" + links[i].href;
     }
  }
}
