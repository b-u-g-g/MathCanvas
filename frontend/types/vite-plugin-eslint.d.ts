declare module 'vite-plugin-eslint' {
  import type { Plugin } from 'vite';

  // Match the plugin's signature (based on its own types)
  interface Options {
    cache?: boolean;
    include?: string | string[];
    exclude?: string | string[];
    formatter?: string;
    emitWarning?: boolean;
    emitError?: boolean;
    failOnWarning?: boolean;
    failOnError?: boolean;
    fix?: boolean;
    lintOnStart?: boolean;
  }

  export default function eslintPlugin(options?: Options): Plugin;
}
