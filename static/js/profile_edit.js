// $(document).ready(function() {
//   $('#profile_image').on('change', function (e) {
//       var reader = new FileReader();
//       reader.onload = function (e) {
//           $("#preview").find("img").attr('src', e.target.result);
//       }
//       reader.readAsDataURL(e.target.files[0]);
//   });
//
//   $('.sns-link').on('click', function (e) {
//       var $form = $("#form");
//       var url = $(e.currentTarget).data("href");
//
//       $form.attr('action', url);
//       $form.submit();
//   });
//
//   $("input").on('change', function (e) {
//       e.target.blur();
//   });
// });