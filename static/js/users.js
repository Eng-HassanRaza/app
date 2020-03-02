$(document).ready(function () {
    // more users
    $('#btn-readmore-users').on("click", function (e) {
       var lastItem = $("#user_list > div:last-child");
       var lastId = lastItem.data("id");
       var hasNext = lastItem.data("has-next") === "True";
       console.log("id=" + lastId + ", hasNext=" + hasNext)
       if (!hasNext) {
         $('#btn-readmore-users').hide();
         return;
       }

       // ajax
       $.ajax({ url: '/api/users?last_id=' + lastId })
       .done(function(response, textStatus, jqXHR) {
           $('#user_list').append(response);

           if ($("#user_list > div:last-child").data("has-next") === "False") {
             $('#btn-readmore-users').hide();
           }
       })
       .fail(function(jqXHR, textStatus, errorThrown) {
//  　　　　　 alert("失敗しました")
            console.error(errorThrown)
       });
       //
    });
});