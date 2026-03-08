import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../api/axios'
import Toast from '../components/Toast'

function PhotoDetail() {
  const { photoId } = useParams()
  const navigate = useNavigate()
  const [photo, setPhoto] = useState(null)
  const [photoUrl, setPhotoUrl] = useState(null)
  const [faces, setFaces] = useState([])
  const [selectedFace, setSelectedFace] = useState(null)
  const [editingFace, setEditingFace] = useState(null)
  const [editName, setEditName] = useState('')
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 })
  const [containerDimensions, setContainerDimensions] = useState({ width: 0, height: 0 })
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)
  const imageRef = useState(null)
  const containerRef = useState(null)

  useEffect(() => {
    fetchPhotoDetails()
  }, [photoId])

  const fetchPhotoDetails = async () => {
    try {
      const [photoRes, facesRes] = await Promise.all([
        api.get(`/photos/${photoId}`, { responseType: 'blob' }),
        api.get(`/photos/${photoId}/faces`)
      ])
      const url = URL.createObjectURL(photoRes.data)
      setPhotoUrl(url)
      setPhoto({ id: photoId })
      setFaces(facesRes.data.faces || [])
      
      // Get image dimensions
      const img = new Image()
      img.onload = () => {
        setImageDimensions({ width: img.width, height: img.height })
      }
      img.src = url
    } catch (err) {
      showToast('Failed to load photo details', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleImageLoad = (e) => {
    const img = e.target
    setContainerDimensions({ width: img.clientWidth, height: img.clientHeight })
  }

  const calculateBoundingBox = (bbox) => {
    if (!bbox || !imageDimensions.width || !containerDimensions.width) return null
    
    const [x, y, w, h] = bbox.split(',').map(Number)
    
    // Calculate scale factors
    const scaleX = containerDimensions.width / imageDimensions.width
    const scaleY = containerDimensions.height / imageDimensions.height
    
    return {
      left: x * scaleX,
      top: y * scaleY,
      width: w * scaleX,
      height: h * scaleY
    }
  }

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this photo?')) return

    try {
      await api.delete(`/photos/${photoId}`)
      showToast('Photo deleted successfully', 'success')
      setTimeout(() => navigate('/gallery'), 1000)
    } catch (err) {
      showToast('Failed to delete photo', 'error')
    }
  }

  const handleEditFace = (face) => {
    setEditingFace(face.id)
    setEditName(face.person_name)
  }

  const handleSaveEdit = async (faceId) => {
    if (!editName.trim()) {
      showToast('Please enter a name', 'error')
      return
    }

    try {
      await api.post('/faces/label', {
        face_id: faceId,
        person_name: editName.trim()
      })
      
      // Update local state
      setFaces(faces.map(f => 
        f.id === faceId ? { ...f, person_name: editName.trim() } : f
      ))
      setEditingFace(null)
      setEditName('')
      showToast('Face label updated!', 'success')
    } catch (err) {
      showToast('Failed to update label', 'error')
    }
  }

  const handleDeleteFace = async (faceId) => {
    if (!confirm('Are you sure you want to remove this face label?')) return

    try {
      await api.delete(`/faces/${faceId}`)
      
      // Remove from local state
      setFaces(faces.filter(f => f.id !== faceId))
      showToast('Face removed successfully', 'success')
    } catch (err) {
      showToast('Failed to remove face', 'error')
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="w-20 h-20 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 font-semibold text-lg">Loading photo...</p>
            <svg className="w-12 h-12 mx-auto mt-2 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold indian-gradient-text mb-2 flex items-center gap-3">
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                <span>Photo Details</span>
              </h1>
              <p className="text-gray-600 font-medium">
                View and manage this photo
              </p>
            </div>
            <button
              onClick={() => navigate('/gallery')}
              className="px-6 py-3 rounded-xl border-2 border-orange-300 bg-white text-orange-600 font-semibold hover:bg-orange-50 transition-all"
            >
              ← Back to Gallery
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Photo */}
          <div className="lg:col-span-2">
            <div className="indian-card p-4">
              <div className="relative aspect-video rounded-xl overflow-hidden border-3 border-orange-300">
                {photoUrl ? (
                  <div className="relative w-full h-full">
                    <img
                      src={photoUrl}
                      alt="Photo"
                      className="w-full h-full object-contain bg-gray-100"
                      onLoad={handleImageLoad}
                    />
                    {/* Face bounding boxes */}
                    {containerDimensions.width > 0 && faces.map((face) => {
                      const bbox = calculateBoundingBox(face.bbox)
                      if (!bbox) return null
                      
                      const isSelected = selectedFace === face.id
                      
                      return (
                        <div
                          key={face.id}
                          onClick={() => setSelectedFace(isSelected ? null : face.id)}
                          className="absolute cursor-pointer transition-all duration-300"
                          style={{
                            left: `${bbox.left}px`,
                            top: `${bbox.top}px`,
                            width: `${bbox.width}px`,
                            height: `${bbox.height}px`,
                            border: isSelected ? '4px solid #FF9933' : '3px solid #FFD700',
                            boxShadow: isSelected 
                              ? '0 0 20px rgba(255, 153, 51, 0.8), inset 0 0 20px rgba(255, 153, 51, 0.3)' 
                              : '0 0 10px rgba(255, 215, 0, 0.6)',
                            backgroundColor: isSelected ? 'rgba(255, 153, 51, 0.2)' : 'rgba(255, 215, 0, 0.1)',
                          }}
                        >
                          {face.person_name && (
                            <div 
                              className="absolute left-0 px-3 py-1 rounded-lg font-bold text-sm whitespace-nowrap"
                              style={{
                                top: bbox.top > 35 ? '-32px' : `${bbox.height + 4}px`,
                                background: isSelected 
                                  ? 'linear-gradient(135deg, #FF9933 0%, #FFA500 100%)'
                                  : 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
                                color: 'white',
                                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
                              }}
                            >
                              {face.person_name}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gray-100">
                    <div className="text-center">
                      <div className="w-12 h-12 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                      <p className="text-gray-600">Loading image...</p>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Instructions */}
              {faces.length > 0 && (
                <div className="mt-4 p-3 rounded-xl bg-gradient-to-r from-orange-50 to-yellow-50 border-2 border-orange-200">
                  <p className="text-sm text-gray-700 font-medium text-center flex items-center justify-center gap-2">
                    <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
                    <span>Click on a face box or name to highlight it</span>
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            {/* Labeled Faces */}
            <div className="indian-card p-6">
              <h2 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                <span>Labeled Faces ({faces.filter(f => f.person_name).length})</span>
              </h2>
              
              {faces.filter(f => f.person_name).length === 0 ? (
                <div className="text-center py-6">
                  <svg className="w-16 h-16 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
                  <p className="text-gray-600 font-medium text-sm">No labeled faces</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {faces.filter(f => f.person_name).map((face, idx) => {
                    const isSelected = selectedFace === face.id
                    const isEditing = editingFace === face.id
                    return (
                      <div
                        key={face.id}
                        className={`p-4 rounded-xl transition-all duration-300 ${
                          isSelected 
                            ? 'bg-gradient-to-r from-orange-400 to-yellow-400 border-3 border-orange-500 shadow-lg' 
                            : 'bg-gradient-to-r from-orange-50 to-yellow-50 border-2 border-orange-200 hover:shadow-md'
                        }`}
                      >
                        {isEditing ? (
                          <div className="space-y-3">
                            <input
                              type="text"
                              value={editName}
                              onChange={(e) => setEditName(e.target.value)}
                              className="indian-input w-full"
                              placeholder="Enter name..."
                              autoFocus
                            />
                            <div className="flex gap-2">
                              <button
                                onClick={() => handleSaveEdit(face.id)}
                                className="flex-1 px-4 py-2 rounded-lg bg-green-500 text-white font-semibold hover:bg-green-600 transition-colors flex items-center justify-center gap-1"
                              >
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/></svg>
                                <span>Save</span>
                              </button>
                              <button
                                onClick={() => {
                                  setEditingFace(null)
                                  setEditName('')
                                }}
                                className="flex-1 px-4 py-2 rounded-lg bg-gray-500 text-white font-semibold hover:bg-gray-600 transition-colors flex items-center justify-center gap-1"
                              >
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"/></svg>
                                <span>Cancel</span>
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className="flex items-center gap-3">
                            <div 
                              onClick={() => setSelectedFace(isSelected ? null : face.id)}
                              className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl cursor-pointer ${
                                isSelected 
                                  ? 'bg-white text-orange-500' 
                                  : 'bg-gradient-to-br from-orange-400 to-yellow-400 text-white'
                              }`}
                            >
                              {idx + 1}
                            </div>
                            <div className="flex-1">
                              <p className={`font-bold text-lg ${isSelected ? 'text-white' : 'text-maroon'}`}>
                                {face.person_name}
                              </p>
                              <p className={`text-sm ${isSelected ? 'text-white/90' : 'text-gray-600'}`}>
                                Confidence: {(face.confidence * 100).toFixed(1)}%
                              </p>
                            </div>
                            {!isSelected && (
                              <div className="flex gap-2">
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    handleEditFace(face)
                                  }}
                                  className="px-3 py-1 rounded-lg bg-blue-500 text-white text-sm font-semibold hover:bg-blue-600 transition-colors flex items-center gap-1"
                                  title="Edit"
                                >
                                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/></svg>
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    handleDeleteFace(face.id)
                                  }}
                                  className="px-3 py-1 rounded-lg bg-red-500 text-white text-sm font-semibold hover:bg-red-600 transition-colors flex items-center gap-1"
                                  title="Delete"
                                >
                                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/></svg>
                                </button>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Unlabeled Faces */}
            {faces.filter(f => !f.person_name).length > 0 && (
              <div className="indian-card p-6">
                <h2 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
                  <svg className="w-7 h-7" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd"/></svg>
                  <span>Unlabeled Faces ({faces.filter(f => !f.person_name).length})</span>
                </h2>
                <div className="space-y-3">
                  {faces.filter(f => !f.person_name).map((face, idx) => {
                    const isSelected = selectedFace === face.id
                    return (
                      <div
                        key={face.id}
                        onClick={() => setSelectedFace(isSelected ? null : face.id)}
                        className={`p-4 rounded-xl cursor-pointer transition-all duration-300 ${
                          isSelected 
                            ? 'bg-gradient-to-r from-yellow-400 to-orange-400 border-3 border-yellow-500 shadow-lg' 
                            : 'bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-200 hover:shadow-md'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl ${
                            isSelected 
                              ? 'bg-white text-yellow-600' 
                              : 'bg-gradient-to-br from-yellow-400 to-orange-400 text-white'
                          }`}>
                            ?
                          </div>
                          <div className="flex-1">
                            <p className={`font-bold text-lg ${isSelected ? 'text-white' : 'text-maroon'}`}>
                              Unknown Person
                            </p>
                            <p className={`text-sm ${isSelected ? 'text-white/90' : 'text-gray-600'}`}>
                              Click to highlight
                            </p>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
                <button
                  onClick={() => navigate('/label-faces')}
                  className="indian-button w-full mt-4 flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
                  <span>Label All Faces</span>
                </button>
              </div>
            )}

            {/* Actions */}
            <div className="indian-card p-6">
              <h2 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
                <svg className="w-7 h-7" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd"/></svg>
                <span>Actions</span>
              </h2>
              
              <div className="space-y-3">
                <button
                  onClick={handleDelete}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-gradient-to-r from-red-500 to-orange-500 text-white font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/></svg>
                  <span>Delete Photo</span>
                </button>
                
                <button
                  onClick={() => navigate('/label-faces')}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
                  <span>Label Faces</span>
                </button>
              </div>
            </div>

            {/* Info */}
            <div className="indian-card p-6 bg-gradient-to-br from-orange-50 to-yellow-50">
              <h2 className="text-2xl font-bold text-maroon mb-4 flex items-center gap-2">
                <svg className="w-7 h-7" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/></svg>
                <span>Information</span>
              </h2>
              <div className="space-y-2 text-gray-700">
                <p className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  <span className="font-medium">Photo ID: {photoId}</span>
                </p>
                <p className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                  <span className="font-medium">{faces.length} face(s) detected</span>
                </p>
                <p className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>
                  <span className="font-medium">
                    {faces.filter(f => f.person_name).length} labeled
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 p-4">
          <div className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
            <span className="text-gray-500 font-medium">Every photo tells a story</span>
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default PhotoDetail
