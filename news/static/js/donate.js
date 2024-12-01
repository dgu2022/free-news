$(document).ready(function(){

    $('#searchbar').focus();

    $('#donate-buttons').on('click', '.btn-blue', function(e) {
      console.log("test1");
      e.preventDefault();
      $('.active').removeClass('active');
      $('#other-input').hide().siblings('#other').show();
      $(this).filter('.btn-blue').addClass("active");
      var value = $(this).data('impact');
      $(this).closest('div').find('p').text("" + value);
      $('#other-input').find('input').val('');  
    });
      
    $('.btn-green').on('click', function() {
      console.log("test2");
      var dollar;
      var input = $('#other-input').find('input').val();
      if ( !input ) {
        dollar = $('.active').data('dollars');
        console.log("test4");
       } else if ( $.trim(input) === '' || isNaN(input)) {
        // empty space leaves value = 'undefined'. 
        // Have to fix $.trim(input) == '' above so that it works.
        console.log('Yes');
        dollar = "Please enter a number."; 
      } else {
        dollar = input;
      }
      $('#price').text(""+dollar);
      
    });

    $('#other').on('click', function(e) {
      console.log("test3");
      e.preventDefault(); 
      var buttons = $(this).parent('#donate-buttons');
      buttons.find('.active').removeClass('active');
      var other = $(this).hide().siblings('#other-input');
      other.show();
      other.find('input').focus();
      var pText = buttons.siblings('p');
      pText.text("아주 감사합니다!");
      var oValue = other.find('input');
      oValue.keyup(function() {
        if ( oValue.val() > 50 ) {
          pText.text("감사합니다!" + " You\'re donation covers housing and counseling services for " + oValue.val()/25 + " people.");
        } else {
          pText.text("감사합니다!");
        }
      });
    }); 

  });