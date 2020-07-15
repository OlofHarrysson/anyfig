module.exports = {
  themes: [
    '@docusaurus/theme-search-algolia',
    '@docusaurus/plugin-google-analytics',
    '@docusaurus/plugin-sitemap',
    {
      cacheTime: 600 * 1000, // 600 sec - cache purge period
      changefreq: 'weekly',
      priority: 0.5,
    },
  ],

  title: 'Anyfig',
  url: 'https://anyfig.now.sh/',
  baseUrl: '/',
  favicon: 'img/logo.svg',
  // favicon: 'img/favicon.ico',
  organizationName: 'OlofHarrysson', // Usually your GitHub org/user name.
  projectName: 'Anyfig', // Usually your repo name.
  themeConfig: {
    // sidebarCollapsible: false,
    defaultDarkMode: true,

    // Google Analytics
    googleAnalytics: {
      trackingID: 'UA-163686450-1',
      anonymizeIP: true,
    },

    // Search
    algolia: {
      appId: 'BH4D9OD16A',
      apiKey: '2482404787a69df7a47eeb3e31da3212',
      indexName: 'anyfig',
      algoliaOptions: {}, // Optional, if provided by Algolia
    },

    // Syntax color theme
    prism: {
      // theme: require('prism-react-renderer/themes/oceanicNext'),
      theme: require('prism-react-renderer/themes/vsDark'),
    },

    navbar: {
      title: 'Anyfig',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },

      links: [{
          to: 'docs/introduction',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },

        {
          to: 'https://github.com/OlofHarrysson/anyfig',
          label: 'Github',
          position: 'left',
        },

        {
          to: 'https://pyfiddle.io/fiddle/4de2f70f-e421-4326-bbb8-b06d5efa547d/?i=true',
          label: 'Online Demo',
          position: 'left',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Olof Harrysson. Built with Docusaurus.`,
    },

  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/OlofHarrysson/anyfig/edit/master/website/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};