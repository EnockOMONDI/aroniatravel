function qtySumary() {
    for (var e = document.getElementsByName("qtyInput"), t = 0, n = 0; n < e.length; n++) parseInt(e[n].value) && (t += parseInt(e[n].value));
}


qtySumary(), $(".qty-btn input").before('<div class="qty-dec"><i class="fa fa-minus"></i></div>'), $(".qty-btn input").after('<div class="qty-inc"><i class="fa fa-plus"></i></div>'), $(".roomBtn input").before('<div class="roomDec"><i class="fa fa-minus"></i></div>'), $(".roomBtn input").after('<div class="roomInc"><i class="fa fa-plus"></i></div>'), $(".qty-dec, .qty-inc").on("click", function() {
    var e = $(this),
        t = e.parent().find("input").val();
    if (e.hasClass("qty-inc")) var n = parseFloat(t) + 1;
    else if (t > 0) n = parseFloat(t) - 1;
    else n = 0;
    e.parent().find("input").val(n), qtySumary()
});