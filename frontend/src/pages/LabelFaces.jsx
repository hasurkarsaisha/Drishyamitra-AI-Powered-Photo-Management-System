import { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import api from '../api/axios'
import Toast from '../components/Toast'

function LabelFaces() {
  const [unlabeledFaces, setUnlabeledFaces] = useState([])
  const [photoUrls, setPhotoUrls] = useState({})
  const [loading, setLoading] = useState(true)
  const [labeling, setLabeling] = useState(null)
  const [personNames, setPersonNames] = useState({}) // Changed to object to store per-face names
  const [toast, setToast] = useState(null)

  useEffect(() => {
    fetchUnlabeledFaces()
  }, [])

  useEffect(() => {
    // Fetch image blobs for all faces
    unlabeledFaces.forEach(face => {
      if (!photoUrls[face.photo_id]) {
        fetchPhotoBlob(face.photo_id)
      }
    })
  }, [unlabeledFaces])

  const fetchPhotoBlob = async (photoId) => {
    try {
      const response = await api.get(`/photos/${photoId}`, {
        responseType: 'blob'
      })
      const url = URL.createObjectURL(response.data)
      setPhotoUrls(prev => ({ ...prev, [photoId]: url }))
    } catch (err) {
      console.error(`Failed to fetch photo ${photoId}:`, err)
    }
  }

  const fetchUnlabeledFaces = async () => {
    try {
      const response = await api.get('/faces/unlabeled')
      setUnlabeledFaces(response.data.unlabeled_faces || [])
    } catch (err) {
      showToast('Failed to fetch unlabeled faces', 'error')
    } finally {
      setLoading(false)
    }
  }

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
  }

  const handleLabel = async (faceId) => {
    const personName = personNames[faceId]
    if (!personName || !personName.trim()) {
      showToast('Please enter a name', 'error')
      return
    }

    setLabeling(faceId)
    try {
      await api.post('/faces/label', {
        face_id: faceId,
        person_name: personName.trim()
      })
      
      setUnlabeledFaces(unlabeledFaces.filter(f => f.id !== faceId))
      setPersonNames(prev => {
        const updated = { ...prev }
        delete updated[faceId]
        return updated
      })
      showToast('Face labeled successfully!', 'success')
    } catch (err) {
      showToast('Failed to label face', 'error')
    } finally {
      setLabeling(null)
    }
  }

  const updatePersonName = (faceId, name) => {
    setPersonNames(prev => ({ ...prev, [faceId]: name }))
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="w-20 h-20 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 font-semibold text-lg">Loading faces...</p>
            <svg className="w-12 h-12 mx-auto mt-2 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="fade-in">
        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

        {/* Header */}
        <div className="indian-card p-6 mb-8 bg-gradient-to-r from-orange-50 to-yellow-50">
          <h1 className="text-4xl font-bold indian-gradient-text mb-2 flex items-center gap-3">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
            <span>Label Faces</span>
          </h1>
          <p className="text-gray-600 font-medium">
            {unlabeledFaces.length} unlabeled faces found
          </p>
          <div className="flex items-center gap-2 mt-2">
            <svg className="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z"/></svg>
            <span className="text-sm text-gray-500">Help AI recognize your loved ones</span>
            <svg className="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z"/></svg>
          </div>
        </div>

        {/* Faces Grid */}
        {unlabeledFaces.length === 0 ? (
          <div className="indian-card p-12 text-center">
            <svg className="w-32 h-32 mx-auto mb-4 text-green-500" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>
            <h2 className="text-3xl font-bold text-maroon mb-3">All Faces Labeled!</h2>
            <p className="text-gray-600 font-medium mb-6">
              Great job! All detected faces have been labeled
            </p>
            <div className="flex items-center justify-center gap-2">
              <svg className="w-8 h-8 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <svg className="w-8 h-8 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
              <svg className="w-8 h-8 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {unlabeledFaces.map((face) => (
              <div key={face.id} className="indian-card p-6">
                <div className="aspect-square rounded-xl overflow-hidden mb-4 border-3 border-orange-300">
                  {photoUrls[face.photo_id] ? (
                    <img
                      src={photoUrls[face.photo_id]}
                      alt="Face"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gray-100">
                      <div className="text-center">
                        <div className="w-8 h-8 border-3 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                        <p className="text-xs text-gray-500">Loading...</p>
                      </div>
                    </div>
                  )}
                </div>
                
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-semibold text-maroon mb-2 flex items-center gap-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                      <span>Person Name</span>
                    </label>
                    <input
                      type="text"
                      value={personNames[face.id] || ''}
                      onChange={(e) => updatePersonName(face.id, e.target.value)}
                      placeholder="Enter name..."
                      className="indian-input w-full"
                      disabled={labeling === face.id}
                    />
                  </div>

                  {face.suggested_person && (
                    <div className="p-3 rounded-xl bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-400">
                      <p className="text-sm font-semibold text-yellow-800 mb-2 flex items-center gap-2">
                        <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
                        <span>AI Suggestion</span>
                      </p>
                      <button
                        onClick={() => updatePersonName(face.id, face.suggested_person.name)}
                        className="w-full px-4 py-2 rounded-lg bg-gradient-to-r from-yellow-400 to-orange-400 text-white font-bold hover:from-yellow-500 hover:to-orange-500 transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                      >
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                        <span>Use "{face.suggested_person.name}"</span>
                      </button>
                    </div>
                  )}

                  <button
                    onClick={() => handleLabel(face.id)}
                    disabled={labeling === face.id || !(personNames[face.id] || '').trim()}
                    className="indian-button w-full flex items-center justify-center gap-2"
                  >
                    {labeling === face.id ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Labeling...</span>
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                        <span>Label Face</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 p-4">
          <div className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
            <span className="text-gray-500 font-medium">Building your family album</span>
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default LabelFaces
