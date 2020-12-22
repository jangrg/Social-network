
export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/topbar/store-black.png' }
    ]
  },
  router: {
    extendRoutes(routes, resolve) {
      routes.push({
        name: 'resetPassword',
        path: '/resetpassword&token=:token',
        component: resolve(__dirname, 'pages/login/resetpassword.vue')
      })
    }
  },
  /*
  ** Customize the progress-bar color
  */
  loading: false,
  /*
  ** Global CSS
  */
  css: [
    '@/static/style.css',
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    'bootstrap-vue/nuxt',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/toast',
    '@nuxtjs/auth',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: process.env.API_URL
  },
  //auth configuration
  auth: {
    cookie: {
      prefix: 'auth.',
      options: {
        expires: 4
      }
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: 'token-auth/', method: 'post', propertyName: 'token' },
          user: { url: 'account/logged_user_data/', method: 'get', propertyName: 'user' },
          logout: false,
        },
        tokenType: 'Token',
      }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      // Added Line
    }
  },
}

