const cards = document.querySelector('.container');

const searchBar = document.forms['search'].querySelector('input');

searchBar.addEventListener('keyup',function(e){
    const inputText = document.forms['search'].querySelector('input').value.toLowerCase();
    const articles = cards.getElementsByClassName('card')

    Array.from(articles).forEach(function(article){
        
       title = article.querySelector('.card-title').textContent.toLowerCase()

       if(title.indexOf(inputText) != -1){
           article.parentElement.style.display = 'flex';
       }
       else{
           article.parentElement.style.display = 'none';
       }
    })
});

