function centerElement(selector) {
        var windowWidth = window.innerWidth;
        var windowHeight = window.innerHeight;
        var $element = $(selector);
        
        var horizontalOffset = $element.width() / 2;
        var verticalOffset   = $element.height() / 2;
        
        var horizontalMidpoint = windowWidth / 2;
        var verticalMidpoint   = windowHeight / 2;
        
        var top = verticalMidpoint - verticalOffset;
        var left = horizontalMidpoint - horizontalOffset;
        
        console.log("HEIGHT: " + $element.width());
        console.log("WIDHT:  " + $element.height());
        
        console.log("HOFFSET: " + horizontalOffset);
        console.log("VOFFSET: " + verticalOffset);
        console.log("HMID:    " + horizontalMidpoint);
        console.log("VMID:    " + verticalMidpoint);
        
        console.log("TOP:     " + top);
        console.log("LEFT:    " + left);
        
        $element.css("top", top);
        $element.css("left", left);
}

function fitImage(imageSelector, containerSelector) {
        var $container = $(containerSelector);
        var maxWidth = $container.width();
        var maxHeight = $container.height();
        
        var $image = $(imageSelector);
        var imageWidth = $image.width();
        var imageHeight = $image.height();
        
        var newWidth = 0;
        var newHeight = 0;
        
        //Is width or height of picture taller?
        if (imageWidth > imageHeight) {
                var ratio = imageHeight/imageWidth;
                console.log("IMAGE IS WIDER");
                console.log("RATIO: " + ratio);
                newWidth = maxWidth;
                newHeight = newWidth*ratio;
        }
        else if (imageWidth < imageHeight) {
                var ratio = imageWidth/imageHeight;
                console.log("IMAGE IS TALLER");
                console.log("RATIO: " + ratio);
                newHeight = maxHeight;
                newWidth = newHeight*(imageWidth/imageHeight);
        }
        else {
                console.log("IMAGE IS SQUARE");
                newHeight = maxHeight;
                newWidth = maxWidth;
        }
        
        //Still not fitting?
        if (newHeight > maxHeight) {
                var ratio = maxHeight/newHeight;
                newHeight = maxHeight;
                newWidth = newWidth * ratio;
        }
        else if (newWidth > maxWidth) {
                var ratio = maxWidth/newWidth;
                newWidth = maxWidth;
                newHeight = newHeight * ratio;
        }
        
        console.log("NEW WIDTH:  " + newWidth);
        console.log("NEW HEIGHT: " + newHeight);
        
        $image.css("width", newWidth);
        $image.css("height", newHeight);
        centerElement("div.image-expand");
}

$(function () {
        centerElement("div.spinner");
		
		$("div.spinner").hide()
        
        $("div#content").hide().waitForImages(function (){
                //$("div.spinner").fadeOut();
                $("div#content").fadeIn();
        });
        
        centerElement("div.flash-message");
                
        $("button.flash-message").click(function() {
                $("div.flash-message").fadeOut("slow");
        });
        
        $("a.post-number").click(function () {
                var postNumber = $(this).html();
                console.log("POST: " + postNumber)
                $("table.new-post textArea").val($("table.new-post textArea").val() + ">>" + postNumber + "\n");
        });
        
        $("img.post-image").click(function () {
                var imageUrl = $(this).attr("image-fullSizeUrl");
                console.log("IMAGE: " + imageUrl);
                
                $("div.image-expand").hide();
                //$("div.spinner").fadeIn();                
                
                $("div.image-expand-inner").html("<img class='image-expand' src='" + imageUrl + "' />").waitForImages(function () {
                        //$("div.spinner").fadeOut(function() {
                                $("div.image-expand").fadeIn();
                                fitImage("img.image-expand", "div.image-expand");
                        //});
                });
        });
        
        $("div.image-expand-inner").click(function () {
                console.log("CLOSE IMAGE!");
                $("div.image-expand").fadeOut(function() {
                        $("div.image-expand-inner").html("");
                        $("div.fullscreen-button").hide();
                });
        });
        
        $("div.fullscreen-button").click(function (){
                console.log("CLICKED FULLSCREEN!");
                var url = $("img.image-expand").attr("src");
                window.location.href = url;
        });
        
        $("div.image-expand").hover(
                function() {
                        console.log("HOVER IN");
                        $("div.fullscreen-button").fadeIn();
                },
                function() {
                        console.log("HOVER OUT");
                        $("div.fullscreen-button").fadeOut();
                });
})