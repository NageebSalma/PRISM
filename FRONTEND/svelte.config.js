import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.
		adapter: adapter({
			pages: 'build', // Directory where the static site is generated
			assets: 'build', // Directory for assets
			fallback: 'index.html', // Optional: For single-page apps, fallback to this file
		}),
		prerender: {
			entries: ['*'], // Pre-render all pages
		  },
	}
};

export default config;
