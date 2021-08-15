function redir(){
    localStorage.setItem('scroll-pos', $(window).scrollTop());
    console.log("Inside redir")
}

var pos = localStorage.getItem('scroll-pos', 0);
if (pos)
    $(window).scrollTop(pos)

localStorage.setItem('scroll-pos', 0);

    