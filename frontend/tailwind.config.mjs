/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        'playfair': ['"Playfair Display"', 'Georgia', 'serif'],
        'outfit': ['Outfit', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        'croisetier': {
          'wood':    '#5C3A1E',
          'gold':    '#C9A84C',
          'cream':   '#F5F0E8',
          'linen':   '#EDE8DC',
          'ink':     '#1A1209',
          'smoke':   '#2C2416',
          'mist':    '#8B7355',
        }
      },
      keyframes: {
        /* Animations héritées */
        'fade-in-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':      { transform: 'translateY(-10px)' },
        },
        /* Nouvelles animations Le Croisetier */
        'shimmer': {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        'slide-in-left': {
          '0%':   { opacity: '0', transform: 'translateX(-40px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'slide-in-right': {
          '0%':   { opacity: '0', transform: 'translateX(40px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'scale-up': {
          '0%':   { opacity: '0', transform: 'scale(0.92)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        'grain': {
          '0%, 100%': { transform: 'translate(0, 0)' },
          '10%':      { transform: 'translate(-2%, -3%)' },
          '30%':      { transform: 'translate(3%, -1%)' },
          '50%':      { transform: 'translate(-1%, 3%)' },
          '70%':      { transform: 'translate(2%, 2%)' },
          '90%':      { transform: 'translate(-3%, 1%)' },
        },
        'draw-stroke': {
          '0%':   { strokeDashoffset: '300' },
          '100%': { strokeDashoffset: '0' },
        },
        'pulse-slow': {
          '0%, 100%': { opacity: '1', transform: 'translateY(0)' },
          '50%':      { opacity: '0.5', transform: 'translateY(6px)' },
        },
        'fade-in': {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'chapter-in': {
          '0%':   { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'gold-shimmer': {
          '0%':   { backgroundPosition: '0% 50%' },
          '50%':  { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
        'ripple': {
          '0%':   { transform: 'scale(0)', opacity: '1' },
          '100%': { transform: 'scale(4)', opacity: '0' },
        },
      },
      animation: {
        'fade-in-up':        'fade-in-up 0.8s ease-out forwards',
        'fade-in-up-delay':  'fade-in-up 0.8s ease-out 0.2s forwards',
        'fade-in-up-delay-2':'fade-in-up 0.8s ease-out 0.4s forwards',
        'float':             'float 6s ease-in-out infinite',
        'shimmer':           'shimmer 2.5s linear infinite',
        'slide-in-left':     'slide-in-left 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'slide-in-right':    'slide-in-right 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'scale-up':          'scale-up 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'grain':             'grain 0.5s steps(1) infinite',
        'draw-stroke':       'draw-stroke 1.5s ease-out forwards',
        'pulse-slow':        'pulse-slow 2s ease-in-out infinite',
        'fade-in':           'fade-in 1s ease-out forwards',
        'chapter-in':        'chapter-in 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'gold-shimmer':      'gold-shimmer 3s ease infinite',
        'ripple':            'ripple 0.6s linear',
      },
      backgroundSize: {
        '200%': '200%',
      }
    },
  },
  plugins: [],
}
