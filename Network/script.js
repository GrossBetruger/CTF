{}
function r() {
    for (var r = 0, e = 0, a = "", l = 0; l < n.length; l++)
        if (n[l].toLowerCase() != n[l] && (r += 1), 8 == ++e) {
            if (!t) return;
            a += String.fromCharCode(r), r = 0, e = 0
        } else r <<= 1;
    return a
}
var e = !1,
    t = !1,
    a = setInterval(function() {
        e && (t = !0, alert("Your flag is: " + r()), clearInterval(a));
        t = !1
    }, 1e3),
    n = "zGWfxPQynEPcZJbcqTEtheaSvSBmhGCJlOQDQwQPiUWllfgCiWAcNKrftWXkCStffMyQEEOBnKSUTbbScLCtAJPXnXBKbLaJaUVZedFdvDiTSDPLeKLffjVjpVXwctdXjWILrzYHzBNyvIcUzHjKKMYMdFQpgfzXoWVBylLvrTVsrFfLvHoQHHSLcTRpytDztnROxkKGrYOmZUocsUBnUWJTxBFvEETwkRMqbAGQlVjMHQREbRuHzIoexUPcYBGOfQtRKGJOuIRIcKwSqHZAbqIGaPXGSOnJ";
}