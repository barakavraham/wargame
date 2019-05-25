;window.webgame = {};

(function($, webgame) {
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

})(jQuery, window.webgame);