$(document).ready(function() {
    // clipboard-polyfill.js
//    $('a.copy').on("click", function(e) {
//      var value = $(e.currentTarget).data("clipboard-text");
//      clipboard.writeText(value)
//      .then(() => alert("「" + value + "」をコピーしました"))
//      .catch(err => {
//        if((err.name) == "NotAllowedError") alert("コピーに失敗しました。権限がありません。");
//        else alert(`コピーに失敗しました。`);
//      });
//    });

    // clipboard.js
    var clipboard = new ClipboardJS('a.copy');

    clipboard.on('success', function(e) {
        alert("「" + e.text + "」をコピーしました")
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
       alert("コピーに失敗しました。");
    });
});