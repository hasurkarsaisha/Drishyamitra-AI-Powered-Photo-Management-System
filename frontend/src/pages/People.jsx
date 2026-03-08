import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import Modal from '../components/Modal'
import api from '../api/axios'

function People() {
  const navigate = useNavigate()
  const [people, setPeople] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedPerson, setSelectedPerson] = useState(null)
  const [personPhotos, setPersonPhotos] = useState([])
  const [photoUrls, setPhotoUrls] = useState({})
  const [loadingPhotos, setLoadingPhotos] = useState(false)

  useEffect(() => {
    fetchPeople()
  }, [])

  const fetchPeople = async () => {
    try {
      const response = await api.get('/photos/people')
      setPeople(response.data.people || [])
    } catch (err) {
      console.error('Failed to fetch people:', err)
    } finally {
      setLoading(false)
    }
  }

  const viewPersonPhotos = async (person) => {
    setSelectedPerson(person)
    setLoadingPhotos(true)
    try {
      const response = await api.get(`/photos/people/${person.id}/photos`)
      setPersonPhotos(response.data.photos || [])
      
      // Fetch photo blobs
      for (const photo of response.data.photos) {
        if (!photoUrls[photo.id]) {
          fetchPhotoBlob(photo.id)
        }
      }
    } catch (err) {
      console.error('Failed to fetch person photos:', err)
    } finally {
      setLoadingPhotos(false)
    }
  }

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

  const closeModal = () => {
    setSelectedPerson(null)
    setPersonPhotos([])
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="w-20 h-20 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600 font-semibold text-lg">Loading people...</p>
            <svg className="w-12 h-12 mx-auto mt-2 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="fade-in">
        {/* Header */}
        <div className="indian-card p-6 mb-8 bg-gradient-to-r from-orange-50 to-yellow-50">
          <h1 className="text-4xl font-bold indian-gradient-text mb-2 flex items-center gap-3">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
            <span>People in Your Gallery</span>
          </h1>
          <p className="text-gray-600 font-medium">
            {people.length} people tagged in your photos
          </p>
          <div className="flex items-center gap-2 mt-2">
            <svg className="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z"/></svg>
            <span className="text-sm text-gray-500">Organize by faces</span>
            <svg className="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z"/></svg>
          </div>
        </div>

        {/* People Grid */}
        {people.length === 0 ? (
          <div className="indian-card p-12 text-center">
            <svg className="w-32 h-32 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            <h2 className="text-3xl font-bold text-maroon mb-3">No People Tagged Yet</h2>
            <p className="text-gray-600 font-medium mb-6">
              Start labeling faces in your photos to see them here
            </p>
            <button
              onClick={() => navigate('/label-faces')}
              className="indian-button inline-flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
              <span>Label Faces Now</span>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {people.map((person) => (
              <div
                key={person.id}
                onClick={() => viewPersonPhotos(person)}
                className="indian-card p-6 cursor-pointer hover-lift text-center group"
              >
                <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-orange-400 to-yellow-400 flex items-center justify-center text-5xl diya-glow group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                </div>
                <h3 className="text-2xl font-bold text-maroon mb-2">{person.name}</h3>
                <div className="flex items-center justify-center gap-2 text-gray-600">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  <span className="font-semibold">{person.photo_count} photos</span>
                </div>
                <div className="mt-4 flex justify-center gap-1">
                  <span className="text-sm">✦</span>
                  <span className="text-sm">✦</span>
                  <span className="text-sm">✦</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 p-4">
          <div className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
            <span className="text-gray-500 font-medium">Connecting faces to memories</span>
            <svg className="w-5 h-5 text-orange-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
          </div>
        </div>

        {/* Photos Modal */}
        {selectedPerson && (
          <Modal isOpen={true} onClose={closeModal} title={`Photos of ${selectedPerson.name}`}>
            {loadingPhotos ? (
              <div className="flex items-center justify-center py-12">
                <div className="text-center">
                  <div className="w-12 h-12 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                  <p className="text-gray-600">Loading photos...</p>
                </div>
              </div>
            ) : personPhotos.length === 0 ? (
              <div className="text-center py-12">
                <svg className="w-24 h-24 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                <p className="text-gray-600 font-medium">No photos found</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-h-[60vh] overflow-y-auto p-4">
                {personPhotos.map((photo) => (
                  <div
                    key={photo.id}
                    onClick={() => {
                      closeModal()
                      navigate(`/photo/${photo.id}`)
                    }}
                    className="aspect-square rounded-xl overflow-hidden border-2 border-orange-200 cursor-pointer hover:border-orange-400 transition-all hover:scale-105"
                  >
                    {photoUrls[photo.id] ? (
                      <img
                        src={photoUrls[photo.id]}
                        alt={photo.filename}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-gray-100">
                        <div className="w-8 h-8 border-3 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Modal>
        )}
      </div>
    </Layout>
  )
}

export default People
