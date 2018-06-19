$(function () {
    $('.cl-save').click(
        function () {
            var dt = new Date();
            set_act($(this));

            kendo.drawing
                .drawDOM("#canvas_data",
                    {
                        forcePageBreak: ".page-break",
                        paperSize: "A3",
                        margin: { left: "4cm", top: "2cm" },
                        scale: 0.55,
                        height: 955,
                        template: $("#page-template").html(),
                        keepTogether: ".prevent-split"
                    })
                .then(function (group) {
                    kendo.drawing.pdf.saveAs(group, "NVH Analysis Report " + dt.toDateString() + ".pdf")
                });
        }
    );
});