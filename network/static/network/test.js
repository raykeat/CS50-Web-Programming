setTimeout(() => {
    console.log(data);
    document.querySelector(`#postcontent-${id}`).innerHTML = newformcontent;
    document.querySelector(`#editdiv2-${id}`).style.display = 'none';
    document.querySelectorAll('#div1').forEach(div => {
      div.style.display = 'block';
    });

    //End console group + adjust delay time 
    console.groupEnd(); 
  }, 3000000); 