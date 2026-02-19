import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkDirective from 'remark-directive';
import { remarkBilingualDirective } from './src/plugins/remark-bilingual.mjs';

export default defineConfig({
  site: 'https://alanhou.org',
  output: 'static',
  integrations: [mdx()],
  redirects: {
    '/installing-odoo-development-environment': '/blog/installing-odoo-development-environment',
    '/managing-odoo-server-instances': '/blog/managing-odoo-server-instances',
    '/server-deployment': '/blog/server-deployment',
    '/creating-odoo-add-on-modules': '/blog/creating-odoo-add-on-modules',
    '/application-models': '/blog/application-models',
    '/basic-server-side-development': '/blog/basic-server-side-development',
    '/odoo12-module-data': '/blog/odoo12-module-data',
    '/debugging': '/blog/debugging',
    '/advanced-server-side-development-techniques': '/blog/advanced-server-side-development-techniques',
    '/backend-views': '/blog/backend-views',
    '/access-security': '/blog/access-security',
    '/internationalization': '/blog/internationalization',
    '/automation-workflows-printouts': '/blog/automation-workflows-printouts',
    '/web-server-development': '/blog/web-server-development',
    '/cms-website-development': '/blog/cms-website-development',
    '/web-client-development': '/blog/web-client-development',
    '/in-app-purchasing-odoo': '/blog/in-app-purchasing-odoo',
    '/automated-test-cases': '/blog/automated-test-cases',
    '/managing-deploying-testing-odoo-sh': '/blog/managing-deploying-testing-odoo-sh',
    '/remote-procedure-calls-odoo': '/blog/remote-procedure-calls-odoo',
    '/performance-optimization': '/blog/performance-optimization',
    '/point-sale': '/blog/point-sale',
    '/manage-emails-odoo': '/blog/manage-emails-odoo',
    '/iot-box': '/blog/iot-box',
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkDirective, remarkBilingualDirective],
    rehypePlugins: [rehypeKatex],
  },
});
