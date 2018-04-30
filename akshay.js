function submitClick(e)
{
     e.preventDefault();
     $("#contactForm").slideUp("slow")', 2000);
}

$(document).ready(function() {
    $('#textbox').click(submitClick);
});