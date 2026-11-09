/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          canvas: '#080C14',
          surface: '#0B111E',
          'surface-card': '#0F172A',
          elevated: '#1E293B',
          hover: '#27354E',
          cyan: '#06B6D4',
          'cyan-hover': '#0891B2',
          blue: '#3B82F6',
          purple: '#8B5CF6',
        },
        threat: {
          safe: '#10B981',
          'safe-hover': '#059669',
          warning: '#F59E0B',
          'warning-hover': '#D97706',
          critical: '#EF4444',
          'critical-hover': '#DC2626',
        },
        slate: {
          white: '#F8FAFC',
          grey: '#94A3B8',
        }
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        ui: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
        kelly: ['"Kelly Slab"', 'serif'],
      },
      boxShadow: {
        'cyan-glow': '0 0 16px rgba(6, 182, 212, 0.4)',
        'cyan-focus': '0 0 20px rgba(6, 182, 212, 0.25)',
      }
    },
  },
  plugins: [],
}
