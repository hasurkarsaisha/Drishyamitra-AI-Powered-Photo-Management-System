import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../api/axios'

function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState({ photos: 0, people: 0, unlabeled: 0 })
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [photosRes, peopleRes, facesRes, userRes] = await Promise.all([
        api.get('/photos/search'),
        api.get('/photos/people'),
        api.get('/faces/unlabeled'),
        api.get('/auth/me')
      ])

      setStats({
        photos: photosRes.data.photos?.length || 0,
        people: peopleRes.data.people?.length || 0,
        unlabeled: facesRes.data.unlabeled_faces?.length || 0
      })
      setUser(userRes.data)
      setError(null)
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err)
      setError(err.response?.data?.error || err.message || 'Failed to load dashboard')
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ icon, label, value, color, onClick }) => (
    <div
      onClick={onClick}
      className="indian-card cursor-pointer hover-lift p-6 text-center"
    >
      <div className={`mb-4 ${color} flex justify-center`}>{icon}</div>
      <h3 className="text-4xl font-bold text-maroon mb-2">{value}</h3>
      <p className="text-gray-600 font-semibold text-lg">{label}</p>
      <div className="mt-4 flex justify-center gap-1">
        <span className="text-sm">✦</span>
        <span className="text-sm">✦</span>
        <span className="text-sm">✦</span>
      </div>
    </div>
  )

  const QuickAction = ({ icon, label, onClick, color }) => (
    <button
      onClick={onClick}
      className={`indian-card p-6 hover-lift flex flex-col items-center gap-3 bg-white border-3 ${color.border} hover:shadow-xl transition-all`}
    >
      <div className={color.text}>{icon}</div>
      <span className={`font-bold text-lg ${color.text}`}>{label}</span>
    </button>
  )

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="w-20 h-20 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 font-semibold text-lg">Loading dashboard...</p>
            <p className="text-2xl mt-2">🪔</p>
          </div>
        </div>
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="indian-card p-8 text-center max-w-md">
            <div className="text-6xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-maroon mb-3">Error Loading Dashboard</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={fetchDashboardData}
              className="indian-button"
            >
              Try Again
            </button>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="fade-in">
        {/* Welcome Header */}
        <div className="indian-card p-8 mb-8 bg-gradient-to-r from-orange-50 to-yellow-50">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-5xl font-bold mb-2 text-maroon">
                नमस्ते, {user?.username || 'Friend'}!
              </h1>
              <p className="text-xl text-gray-600 font-medium">
                Welcome to your photo gallery dashboard
              </p>
              <div className="flex items-center gap-2 mt-3">
                <span className="text-2xl">🌺</span>
                <span className="text-gray-500 font-medium">Manage your memories with tradition</span>
                <span className="text-2xl">🌺</span>
              </div>
            </div>
            <div className="text-8xl diya-glow">
              🪔
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon={<svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>}
            label="Total Photos"
            value={stats.photos}
            color="text-orange-500"
            onClick={() => navigate('/gallery')}
          />
          <StatCard
            icon={<svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>}
            label="People Tagged"
            value={stats.people}
            color="text-green-600"
            onClick={() => navigate('/people')}
          />
          <StatCard
            icon={<svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>}
            label="Unlabeled Faces"
            value={stats.unlabeled}
            color="text-yellow-600"
            onClick={() => navigate('/label-faces')}
          />
        </div>

        {/* Decorative Divider */}
        <div className="indian-divider my-8"></div>

        {/* Quick Actions */}
        <div>
          <h2 className="text-3xl font-bold text-maroon mb-6 text-center">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <QuickAction
              icon={<svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>}
              label="Upload Photos"
              onClick={() => navigate('/gallery')}
              color={{ text: 'text-orange-600', border: 'border-orange-400' }}
            />
            <QuickAction
              icon={<svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>}
              label="Label Faces"
              onClick={() => navigate('/label-faces')}
              color={{ text: 'text-green-600', border: 'border-green-400' }}
            />
            <QuickAction
              icon={<svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>}
              label="AI Assistant"
              onClick={() => navigate('/chat')}
              color={{ text: 'text-blue-600', border: 'border-blue-400' }}
            />
            <QuickAction
              icon={<svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
              label="View History"
              onClick={() => navigate('/history')}
              color={{ text: 'text-purple-600', border: 'border-purple-400' }}
            />
          </div>
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <div className="indian-card p-6 bg-gradient-to-br from-orange-50 to-yellow-50">
            <h3 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-maroon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>Features</span>
            </h3>
            <ul className="space-y-3">
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/></svg>
                <span className="font-semibold text-gray-800">AI-powered face recognition</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/></svg>
                <span className="font-semibold text-gray-800">Smart photo organization</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/></svg>
                <span className="font-semibold text-gray-800">Natural language search</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/></svg>
                <span className="font-semibold text-gray-800">Secure cloud storage</span>
              </li>
            </ul>
          </div>

          <div className="indian-card p-6 bg-gradient-to-br from-green-50 to-emerald-50">
            <h3 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-maroon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
              <span>Tips</span>
            </h3>
            <ul className="space-y-3">
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-yellow-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                <span className="font-semibold text-gray-800">Upload clear, well-lit photos</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-yellow-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                <span className="font-semibold text-gray-800">Label faces for better search</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-yellow-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                <span className="font-semibold text-gray-800">Use AI chat for quick finds</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-5 h-5 text-yellow-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                <span className="font-semibold text-gray-800">Organize by people & events</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 p-6 indian-card bg-gradient-to-r from-orange-50 to-yellow-50">
          <p className="text-gray-600 font-medium text-lg">
            Thank you for using DrishyaMitra
          </p>
          <p className="text-sm text-gray-500 mt-2">Preserving memories with tradition</p>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
