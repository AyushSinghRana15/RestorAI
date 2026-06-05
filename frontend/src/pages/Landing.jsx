import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'

const features = [
  { title: 'Face Restoration', desc: 'Restore facial details with GFPGAN while preserving identity' },
  { title: 'Scratch Removal', desc: 'Remove scratches and damaged regions using LaMa inpainting' },
  { title: 'Super Resolution', desc: 'Upscale low-resolution images with Real-ESRGAN' },
  { title: 'Colorization', desc: 'Colorize black-and-white photos using DeOldify' },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Navbar />

      <section className="flex flex-col items-center justify-center px-4 pt-24 pb-16 text-center">
        <h1 className="text-5xl font-bold text-gray-900">RestorAI</h1>
        <p className="max-w-xl mt-4 text-lg text-gray-600">
          Repair, Enhance, and Colorize Old Photographs Using Advanced Deep Learning Models
        </p>
        <p className="mt-2 text-gray-500">Restore Memories with AI</p>
        <div className="flex gap-4 mt-8">
          <Link
            to="/dashboard"
            className="px-6 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition"
          >
            Upload Image
          </Link>
          <Link
            to="/dashboard"
            className="px-6 py-3 text-gray-700 bg-white border rounded-lg hover:bg-gray-50 transition"
          >
            View Demo
          </Link>
        </div>
      </section>

      <section className="px-4 pb-24">
        <div className="grid max-w-4xl grid-cols-1 gap-6 mx-auto sm:grid-cols-2">
          {features.map((f) => (
            <div key={f.title} className="p-6 bg-white rounded-xl shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">{f.title}</h3>
              <p className="mt-2 text-sm text-gray-600">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="pb-24 text-center">
        <div className="flex items-center justify-center gap-8 text-sm font-medium text-gray-500">
          <span>Upload</span>
          <span>→</span>
          <span>Restore</span>
          <span>→</span>
          <span>Compare</span>
          <span>→</span>
          <span>Download</span>
        </div>
      </section>
    </div>
  )
}
