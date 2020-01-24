let version = '0004'
let themeDirectory = '/wp-content/themes/digitalgendergaps'
let imageDirectory = '/assets/images'
let imagePath = themeDirectory + imageDirectory
let cssPath = themeDirectory + '/assets/css'
let jsPath = themeDirectory + '/assets/js'

let appCaches = [{
    name: 'pages-cache-' + version,
    urls: [
      '/',
      '/data/',
      '/updates/',
      '/project/',
      '/indicators/',
      '/team/',
      '/offline/',
      themeDirectory + '/style.css',
      cssPath + '/dashboard.css',
      jsPath + '/dashboard.js',
      //themeDirectory + '/manifest.json',
      //jsPath + '/dashboard.js',
    ]
  },
  {
    name: 'images-cache-' + version,
    urls: [
      imagePath + '/oxweb-logo-rect.svg',
      imagePath + '/qcri28rgb29-01.svg',
      imagePath + '/data2x-logo.png',
      imagePath + '/Icons-mini-icon_world.gif'
    ]
  },
  {
    name: 'third-party-js-cache-' + version,
    urls: [
    ]
  },
  {
    name: 'data-cache-' + version,
    urls: [
    ]
  },
];

self.addEventListener('install', function(event) {
  event.waitUntil(Promise.all(
    appCaches.map(function (cacheData) {
      return caches.open(cacheData.name).then(function (cache) {
        return cache.addAll(cacheData.urls);
      })
    })
  ));
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if ((response) && (event.request.url !== 'https://s3.eu-west-3.amazonaws.com/www.digitalgendergaps.org/data/models.json')) {
          return response;
        }
        else
        {
          //return response;
        }

        return fetch(event.request).then(
          function (response) {
            // Check if we received a valid response
            if (!response || response.status !== 200 || (response.type !== 'basic' && response.type !== 'cors')) {
              if (event.request.url === 'https://s3.eu-west-3.amazonaws.com/www.digitalgendergaps.org/data/models.json') {
				caches.open('data-cache-' + version).then(function(cache) {
				  cache.keys().then(function(keys) {
				    let indexjson = {}
					keys.forEach(function(request, index, array) {
					  indexjson[request] = request;
					});
                    return new Response(JSON.stringify(indexjson), {
                      headers: {'Content-Type': 'application/json'}
                    });
				  });
				})
              }
              return response;
            }
            // cors

            // IMPORTANT: Clone the response. A response is a stream
            // and because we want the browser to consume the response
            // as well as the cache consuming the response, we need
            // to clone it so we have two streams.
            let responseToCache = response.clone();

            let cacheName = null;

            if (response.type === 'basic'){
              cacheName = 'pages-cache-' + version;
            } else if (response.headers.get('Content-Type').indexOf('application/javascript') !== -1) {
              cacheName = 'third-party-js-cache-' + version;
            } else if (event.request.headers.get('Accept').indexOf('application/javascript') !== -1) {
              cacheName = 'third-party-js-cache-' + version;
            } else if (response.headers.get('Content-Type').indexOf('image') !== -1) {
              cacheName = 'images-cache-' + version;
            } else if (event.request.headers.get('Accept').indexOf('image') !== -1) {
              cacheName = 'images-cache-' + version;
            } else if (response.headers.get('Content-Type').indexOf('binary/octet-stream') !== -1) {
              cacheName = 'data-cache-' + version;
            } else if (event.request.headers.get('Accept').indexOf('application/json') !== -1) {
              cacheName = 'data-cache-' + version;
            } else if (event.request.headers.get('Accept').indexOf('text/csv') !== -1) {
              cacheName = 'data-cache-' + version;
            } else if (event.request.url === 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css') {
              cacheName = 'third-party-js-cache-' + version;
            } else if (event.request.url === 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js') {
              cacheName = 'third-party-js-cache-' + version;
            } else {
              console.log(response);
              return response;
            }

            caches.open(cacheName)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});

self.addEventListener('activate', function(event) {

  let cacheWhitelist = appCaches.map(cache => cache.name);

  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
