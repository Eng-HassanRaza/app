$(document).ready(function () {
    // more instagram
    $('#btn-readmore-ig').on("click", function (e) {
       console.log("onClick Instagram");

       var lastItem = $("#ig_list > .item:last-child");
       var lastId = lastItem.data("id");
       var hasNext = lastItem.data("has-next") === "True";
       console.log("id=" + lastId + ", hasNext=" + hasNext)
       if (!hasNext) {
         $('#btn-readmore-ig').hide();
         return;
       }

       console.log("id=" + lastId + " is hasNext")
       // ajax
       var account = $('#btn-readmore-ig').data("id")
       $.ajax({ url: '/profile/' + account + '/ig?last_id=' + lastId })
       .done(function(response, textStatus, jqXHR) {
           $('#ig_list').append(response);

           if ($("#ig_list > .item:last-child").data("has-next") === "False") {
             $('#btn-readmore-ig').hide();
           }
       })
       .fail(function(jqXHR, textStatus, errorThrown) {
  　　　　　 alert("失敗しました")
            console.error(errorThrown)
       });
       //
    });


    // more youtube
    $('#btn-readmore-yt').on("click", function (e) {
       console.log("onClick Youtube");

       var lastItem = $("#yt_list > .box_video_item:last-child");
       var lastId = lastItem.data("id");
       var hasNext = lastItem.data("has-next") === "True";
       console.log("id=" + lastId + ", hasNext=" + hasNext)
       if (!hasNext) {
         $('#btn-readmore-yt').hide();
         return;
       }

       console.log("id=" + lastId + " has Next")

       // ajax
       var account = $('#btn-readmore-yt').data("id")
       $.ajax({ url: '/profile/' + account + '/yt?last_id=' + lastId })
       .done(function(response, textStatus, jqXHR) {
           $('#yt_list').append(response);

           if ($("#yt_list > .box_video_item:last-child").data("has-next") === "False") {
             $('#btn-readmore-yt').hide();
           }
       })
       .fail(function(jqXHR, textStatus, errorThrown) {
  　　　　　 alert("失敗しました")
            console.error(errorThrown)
       });
       //
    });
});