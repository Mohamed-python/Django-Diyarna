  window.addEventListener('load', function() {
    var myCarousel = document.querySelector('#carouselExampleCaptions');
    var carousel = new bootstrap.Carousel(myCarousel, {
      interval: 4000, // كل 3 ثواني
      ride: 'carousel'  // يبدأ تلقائي
    });
  });