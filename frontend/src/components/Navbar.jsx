import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-white shadow-sm">
      <Link to="/" className="text-xl font-bold text-gray-900">
        RestorAI
      </Link>
      <div className="flex items-center gap-6">
        <Link to="/" className="text-gray-600 hover:text-gray-900">Home</Link>
        <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
        <a href="https://github.com/AyushSinghRana15/RestorAI" target="_blank" rel="noreferrer" className="text-gray-600 hover:text-gray-900">
          GitHub
        </a>
      </div>
    </nav>
  )
}
