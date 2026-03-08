import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Gallery from './pages/Gallery'
import People from './pages/People'
import Chat from './pages/Chat'
import History from './pages/History'
import LabelFaces from './pages/LabelFaces'
import PhotoDetail from './pages/PhotoDetail'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return !!localStorage.getItem('token')
  })

  const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('token')
    return token ? children : <Navigate to="/login" />
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={
          <PrivateRoute>
            <Navigate to="/dashboard" replace />
          </PrivateRoute>
        } />
        
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        
        <Route path="/gallery" element={
          <PrivateRoute>
            <Gallery />
          </PrivateRoute>
        } />
        
        <Route path="/people" element={
          <PrivateRoute>
            <People />
          </PrivateRoute>
        } />
        
        <Route path="/chat" element={
          <PrivateRoute>
            <Chat />
          </PrivateRoute>
        } />
        
        <Route path="/history" element={
          <PrivateRoute>
            <History />
          </PrivateRoute>
        } />
        
        <Route path="/label-faces" element={
          <PrivateRoute>
            <LabelFaces />
          </PrivateRoute>
        } />
        
        <Route path="/photo/:photoId" element={
          <PrivateRoute>
            <PhotoDetail />
          </PrivateRoute>
        } />
      </Routes>
    </Router>
  )
}

export default App
