/*
|======================|
| i18n VS util.getLang |
|======================|
| i18n translates the  |
| ui.  GetLang is for  |
| getting activity     |
| data in the users    |
| current language.    |
|======================|
*/

// Add avaliable languages here
var langsAvaliable = [];

var getLangToUse = function () {
  var ul = navigator.language || navigator.userLanguage;

  if ( langsAvaliable.indexOf( ul ) !== -1 ) {
    return ul;
  };

  for ( var i in langsAvaliable ) {
    var l = langsAvaliable[i];
    if ( l.substr( 0, 2 ) == ul.substr( 0, 2 ) ) {
      return l;
    };
  }

  return null;
};

exports.setup = function () {
  l = getLangToUse();
  if ( l === null ) {
    return;
  };

  var url = "translations/" + l + ".json";
  $.get( url ).done( function ( data ) {
    $( "body" ).data( "translations", data );
	translateBody( data );
  });
};

var translateBody = function ( tdata ) {
  $( "*[i18n-content]" ).each( function () {
    var e = $( this );
    if ( e.html().trim() in tdata) {
      e.html( tdata[e.html().trim()] )
    };
  });

  $( "*[i18n-title]" ).each( function () {
    var e = $( this )
    if ( e.attr( "title" ).trim() in tdata) {
      e.attr( "title", tdata[e.attr( "title" ).trim()] )
    };
  });

  $( "*[i18n-placeholder]" ).each( function () {
    var e = $( this )
    if ( e.attr( "placeholder" ).trim() in tdata) {
      e.attr( "placeholder", tdata[e.attr( "placeholder" ).trim()] )
    };
  });
};

exports.get = function ( text ) {
  var data = $( "body" ).data( "translations" );
  if ( text.trim() in data ) {
    return data[text.trim()];
  }
  return text.trim();
}
