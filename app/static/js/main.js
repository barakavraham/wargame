;window.webgame = {};

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

(function($, webgame) {

    let $navbarToggler = $('button.navbar-toggler');

    function setupNavbar() {
        $navbarToggler.on('click', function() {
            $navbarToggler.toggleClass('active');
        });
    }

    $.each( [ "get", "post", "put", "delete" ], function( i, method ) {
        $[ 'gameApi' + _.capitalize(method) ] = function( url, data, callback, dataType ) {
            if (_.isString(url)) {
                url = '/api/' + url;
            }

            // Shift arguments if data argument was omitted
            if ( $.isFunction( data ) ) {
                callback = data;
                data = undefined;
            }

            // The url can be an options object (which then must have .url)
            return $.ajax( $.extend( {
                url: url,
                type: method,
                data: JSON.stringify(data),
                contentType: 'application/json',
                dataType: dataType || 'json',
                success: callback
            }, $.isPlainObject( url ) && url ) );
        };
    });

    setupNavbar();

})(jQuery, window.webgame);