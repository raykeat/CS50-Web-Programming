
function redirect1() {
    window.location.href = "https://about.google/?fg=1&utm_source=google-SG&utm_medium=referral&utm_campaign=hp-header";
  }

function redirect2() {
     window.location.href = "https://store.google.com/SG/?utm_source=hp_header&utm_medium=google_ooo&utm_campaign=GS100042&hl=en-SG";
  }

function googlesearch() {
    const query = document.getElementById("searchinput").value;
    const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
    window.location.href = searchUrl;
}

function redirectfirstresult() {
    const query = document.getElementById("searchinput").value;
    const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&btnI=1`;
    window.location.href = searchUrl;
}

function googleimagesearch() {
  const query = document.getElementById("searchinput").value;
  const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&tbm=isch`;
  window.location.href = searchUrl;
}

function advancedsearch1(){
  const query = document.querySelector('#all').value;
  const searchUrl = 'https://www.google.com/search?q=' + encodeURIComponent(query);
  window.location.href = searchUrl;
}

function advancedsearch2(){
  const query = document.querySelector('#this').value;
  console.log(query);
  const searchUrl = 'https://www.google.com/search?q=' + encodeURIComponent('"' + query + '"');
  window.location.href = searchUrl;
}



function advancedsearch3(){
  const query = document.querySelector('#any').value;
  const searchUrl = 'https://www.google.com/search?as_q=&as_epq=' + encodeURIComponent("query");
  window.location.href = searchUrl;
}

function advancedsearch4(){
  const query = document.querySelector('#none').value;
  const searchUrl = 'https://www.google.com/search?as_q=&as_epq' + encodeURIComponent("query");
  window.location.href = searchUrl;
}