import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../api/axios'
import Toast from '../components/Toast'

function Gallery() {
  const navigate = useNavigate()
  const [photos, setPhotos] = useState([])
  const [photoUrls, setPhotoUrls] = useState({})
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState({ current: 0, total: 0 })
  const [deleting, setDeleting] = useState(null)
  const [toast, setToast] = useState(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    fetchPhotos()
  }, [])

  useEffect(() => {
    // Fetch image blobs for all photos
    photos.forEach(photo => {
      if (!photoUrls[photo.id]) {
        fetchPhotoBlob(photo.id)
      }
    })
  }, [photos])

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

  const fetchPhotos = async () => {
    try {
      const response = await api.get('/photos/search')
      setPhotos(response.data.photos || [])
    } catch (err) {
      showToast('Failed to fetch photos', 'error')
    } finally {
      setLoading(false)
    }
  }

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
  }

  const handleUpload = async (e) => {
    const files = Array.from(e.target.files)
    if (files.length === 0) return

    setUploading(true)
    setUploadProgress({ current: 0, total: files.length })
    let successCount = 0
    let failCount = 0

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        setUploadProgress({ current: i + 1, total: files.length })
        
        const formData = new FormData()
        formData.append('file', file)
        
        try {
          await api.post('/photos/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          successCount++
        } catch (err) {
          failCount++
          console.error(`Failed to upload ${file.name}:`, err)
        }
      }
      
      if (successCount > 0) {
        showToast(`Successfully uploaded ${successCount} photo${successCount > 1 ? 's' : ''}!`, 'success')
        fetchPhotos()
      }
      if (failCount > 0) {
        showToast(`Failed to upload ${failCount} photo${failCount > 1 ? 's' : ''}`, 'error')
      }
    } catch (err) {
      showToast('Failed to upload photos', 'error')
    } finally {
      setUploading(false)
      setUploadProgress({ current: 0, total: 0 })
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleDelete = async (photoId, e) => {
    e.stopPropagation()
    if (!confirm('Are you sure you want to delete this photo?')) return
    
    setDeleting(photoId)
    try {
      await api.delete(`/photos/${photoId}`)
      setPhotos(photos.filter(p => p.id !== photoId))
      showToast('Photo deleted successfully', 'success')
    } catch (err) {
      showToast('Failed to delete photo', 'error')
    } finally {
      setDeleting(null)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="w-20 h-20 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 font-semibold text-lg">Loading gallery...</p>
            <svg className="w-12 h-12 mx-auto mt-2 text-pink-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z"/></svg>
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
                <span>Photo Gallery</span>
              </h1>
              <p className="text-gray-600 font-medium">
                {photos.length} photos in your collection
              </p>
            </div>
            <div className="flex items-center gap-3">
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept="image/*"
                onChange={handleUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className="indian-button flex items-center gap-2"
              >
                {uploading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Uploading...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
                    <span>Upload Photos</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Photos Grid */}
        {photos.length === 0 ? (
          <div className="indian-card p-12 text-center">
            <svg className="w-32 h-32 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <h2 className="text-3xl font-bold text-maroon mb-3">No Photos Yet</h2>
            <p className="text-gray-600 font-medium mb-6">
              Start building your collection by uploading your first photo
            </p>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="indian-button inline-flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span>Upload Your First Photo</span>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {photos.map((photo) => (
              <div
                key={photo.id}
                onClick={() => navigate(`/photo/${photo.id}`)}
                className="indian-card p-3 cursor-pointer hover-lift group"
              >
                <div className="relative aspect-square rounded-xl overflow-hidden mb-3 border-2 border-orange-200">
                  {photoUrls[photo.id] ? (
                    <img
                      src={photoUrls[photo.id]}
                      alt={photo.filename}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gray-100">
                      <div className="text-center">
                        <div className="w-8 h-8 border-3 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                        <p className="text-xs text-gray-500">Loading...</p>
                      </div>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div className="absolute bottom-2 left-2 right-2 flex items-center justify-between">
                      <span className="text-white text-sm font-semibold">View Details</span>
                      <button
                        onClick={(e) => handleDelete(photo.id, e)}
                        disabled={deleting === photo.id}
                        className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm font-semibold transition-colors"
                      >
                        {deleting === photo.id ? '...' : (
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/></svg>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <p className="text-sm text-gray-600 font-medium truncate">
                    {photo.filename}
                  </p>
                  <span className="text-xs text-gray-500">
                    {photo.processed ? '✓' : '⏳'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 p-4">
          <div className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
            <span className="text-gray-500 font-medium">Your memories, preserved with care</span>
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
          </div>
        </div>

        {/* Upload Progress Overlay */}
        {uploading && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="indian-card p-8 max-w-md w-full mx-4">
              <h3 className="text-2xl font-bold text-maroon mb-4 text-center">Uploading Photos</h3>
              <div className="mb-4">
                <div className="flex justify-between text-sm font-semibold text-gray-700 mb-2">
                  <span>Progress</span>
                  <span>{uploadProgress.current} / {uploadProgress.total}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-orange-400 to-yellow-400 transition-all duration-300 rounded-full"
                    style={{ width: `${(uploadProgress.current / uploadProgress.total) * 100}%` }}
                  ></div>
                </div>
              </div>
              <div className="flex items-center justify-center gap-2 text-gray-600">
                <div className="w-6 h-6 border-3 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
                <span className="font-medium">Please wait...</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default Gallery
