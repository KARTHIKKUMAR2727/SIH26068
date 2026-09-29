import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import {
  Bell,
  CloudRain,
  Droplets,
  Gauge,
  LocateFixed,
  MessageSquareText,
  Mic,
  Search,
  ShieldAlert,
  SunMedium,
  Thermometer,
  Volume2,
  Wind,
} from 'lucide-react'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import './App.css'

type WeatherResponse = {
  location: { name: string; latitude: number; longitude: number; country?: string }
  temperature: { current: number; feels_like: number; unit: string }
  humidity: { value: number; unit: string }
  wind: { speed: number; direction: number; gust: number; unit: string }
  pressure: { value: number; unit: string }
  visibility: { value: number; unit: string }
  precipitation: { current: number; probability: number; unit: string }
  condition: string
  condition_code: number
  timestamp: string
  source: { source: string; forecast_model?: string; retrieved_at?: string; data_type?: string; is_demo?: boolean }
}

type ForecastResponse = {
  location: { name: string; latitude: number; longitude: number; country?: string }
  hourly: Array<{
    time: string
    temperature: number
    feels_like: number
    rain_probability: number
    precipitation_mm: number
    humidity: number
    wind_speed: number
    cloud_cover: number
    condition: string
    pressure: number
  }>
  daily: Array<{
    date: string
    temp_max: number
    temp_min: number
    rain_probability: number
    precipitation_sum_mm: number
    humidity_mean: number
    wind_speed_max: number
    condition: string
  }>
  source: { source: string; forecast_model?: string }
}

type ChatApiResponse = {
  response?: string
  answer?: string
  intent?: string
  location?: string | Record<string, unknown>
  source?: string
  language?: string
}

type LanguageOption = {
  code: string
  label: string
  voice: string
}

const API_BASE = 'http://localhost:8000/api'

const languageOptions: LanguageOption[] = [
  { code: 'en', label: 'English', voice: 'en-US' },
  { code: 'hi', label: 'हिन्दी', voice: 'hi-IN' },
  { code: 'ta', label: 'தமிழ்', voice: 'ta-IN' },
  { code: 'te', label: 'తెలుగు', voice: 'te-IN' },
  { code: 'ml', label: 'മലയാളം', voice: 'ml-IN' },
  { code: 'kn', label: 'ಕನ್ನಡ', voice: 'kn-IN' },
  { code: 'bn', label: 'বাংলা', voice: 'bn-IN' },
  { code: 'mr', label: 'मराठी', voice: 'mr-IN' },
]

const getLanguageMeta = (code: string) => languageOptions.find((lang) => lang.code === code) ?? languageOptions[0]

const defaultWeather: WeatherResponse = {
  location: { name: 'Chennai', latitude: 13.0827, longitude: 80.2707, country: 'India' },
  temperature: { current: 31.4, feels_like: 34.2, unit: '°C' },
  humidity: { value: 72, unit: '%' },
  wind: { speed: 16.8, direction: 120, gust: 24, unit: 'km/h' },
  pressure: { value: 1011.2, unit: 'hPa' },
  visibility: { value: 8.5, unit: 'km' },
  precipitation: { current: 0.3, probability: 42, unit: 'mm' },
  condition: 'Partly cloudy',
  condition_code: 2,
  timestamp: new Date().toISOString(),
  source: { source: 'Open-Meteo Meteorological Feed', forecast_model: 'ECMWF Blend', data_type: 'observation' },
}

const defaultForecast: ForecastResponse = {
  location: { name: 'Chennai', latitude: 13.0827, longitude: 80.2707, country: 'India' },
  hourly: [
    { time: 'Now', temperature: 31.4, feels_like: 34.2, rain_probability: 42, precipitation_mm: 0.4, humidity: 72, wind_speed: 17, cloud_cover: 58, condition: 'Partly cloudy', pressure: 1011 },
    { time: '14:00', temperature: 32.6, feels_like: 35.8, rain_probability: 55, precipitation_mm: 0.9, humidity: 68, wind_speed: 18, cloud_cover: 64, condition: 'Rain likely', pressure: 1010 },
    { time: '17:00', temperature: 30.9, feels_like: 33.1, rain_probability: 60, precipitation_mm: 1.2, humidity: 74, wind_speed: 19, cloud_cover: 70, condition: 'Thunderstorm', pressure: 1009 },
    { time: '20:00', temperature: 29.2, feels_like: 31.0, rain_probability: 48, precipitation_mm: 0.7, humidity: 78, wind_speed: 15, cloud_cover: 66, condition: 'Showers', pressure: 1010 },
  ],
  daily: [
    { date: 'Mon', temp_max: 32.1, temp_min: 27.4, rain_probability: 44, precipitation_sum_mm: 1.5, humidity_mean: 73, wind_speed_max: 20, condition: 'Cloudy' },
    { date: 'Tue', temp_max: 33.4, temp_min: 28.2, rain_probability: 58, precipitation_sum_mm: 3.6, humidity_mean: 72, wind_speed_max: 22, condition: 'Rain' },
    { date: 'Wed', temp_max: 34.0, temp_min: 28.8, rain_probability: 42, precipitation_sum_mm: 1.8, humidity_mean: 69, wind_speed_max: 17, condition: 'Sunny' },
    { date: 'Thu', temp_max: 32.7, temp_min: 27.3, rain_probability: 65, precipitation_sum_mm: 4.1, humidity_mean: 76, wind_speed_max: 25, condition: 'Storm risk' },
  ],
  source: { source: 'Open-Meteo Forecast Engine', forecast_model: 'ECMWF/GFS Blend' },
}

const getConditionIcon = (condition: string) => {
  if (condition.toLowerCase().includes('rain') || condition.toLowerCase().includes('storm')) return <CloudRain size={24} />
  if (condition.toLowerCase().includes('sun')) return <SunMedium size={24} />
  return <CloudRain size={24} />
}

function App() {
  const [city, setCity] = useState('')
  const [weather, setWeather] = useState<WeatherResponse>(defaultWeather)
  const [forecast, setForecast] = useState<ForecastResponse>(defaultForecast)
  const [chatInput, setChatInput] = useState('Will it rain today?')
  const [chatAnswer, setChatAnswer] = useState('WeatherGPT is ready. Ask about rain, heat, alerts, or climate patterns in your location.')
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('en')
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)

  const quickPrompts = [
    'Will it rain today in Chennai?',
    'What is the temperature in Mumbai?',
    'Are there any alerts near Coimbatore?',
    'Will the wind be strong tomorrow?',
  ]

  const speakAnswer = (text: string) => {
    if (!text || typeof window === 'undefined') return
    const synth = window.speechSynthesis
    if (!synth) return

    synth.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = getLanguageMeta(language).voice
    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = () => setIsSpeaking(false)
    synth.speak(utterance)
  }

  const stopSpeaking = () => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }

  const fetchWeatherData = async (query = city) => {
    setLoading(true)
    try {
      const weatherRes = await axios.get(`${API_BASE}/weather/current`, { params: { city: query } })
      const forecastRes = await axios.get(`${API_BASE}/forecast`, { params: { city: query } })
      setWeather(weatherRes.data)
      setForecast(forecastRes.data)
    } catch (error) {
      console.error('Weather fetch error:', error)
      setWeather(defaultWeather)
      setForecast(defaultForecast)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    await fetchWeatherData(city)
  }

  const sanitizeDisplayText = (text: string) => {
    if (!text) return text

    const emojiTokens = ['📅', '📊', '🌤️', '🌧️', '⚠️', '📚', '🌾', '🌦️', 'ℹ️', '💡', '🔴', '🟡', '✅', '📍', '📈', '🌡️', '📉', '🌍', '☀️', '⚡', '🛣️', '🚤', '✈️', '🌊']
    let cleaned = text

    for (const token of emojiTokens) {
      cleaned = cleaned.replaceAll(token, '')
    }

    cleaned = cleaned.replace(/\*\*|\*|_/g, '')
    cleaned = cleaned.replace(/\u2022/g, '')
    cleaned = cleaned.replace(/\s{2,}/g, ' ')
    return cleaned.trim()
  }

  const handleAskWeatherGPT = async () => {
    if (!chatInput.trim()) return

    try {
      const response = await axios.post<ChatApiResponse>(`${API_BASE}/chat`, {
        message: chatInput,
        language,
        location: {
          name: city,
          latitude: weather.location.latitude,
          longitude: weather.location.longitude,
        },
      })

      const answer = sanitizeDisplayText(String(response.data?.response || response.data?.answer || 'No answer available.'))
      setChatAnswer(answer)
      speakAnswer(answer)
    } catch (error) {
      console.error('Chat error:', error)
      const fallback = 'The weather intelligence service is currently unavailable. Please try again in a moment.'
      setChatAnswer(fallback)
    }
  }

  const handleVoiceInputToggle = () => {
    const SpeechRecognitionCtor = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

    if (!SpeechRecognitionCtor) {
      setChatAnswer('Voice input is not supported in this browser. Please use text input or use Chrome/Edge with microphone permission enabled.')
      return
    }

    if (isListening) {
      const recognition = (window as any).__weather_gpt_recognition
      if (recognition) {
        recognition.stop()
      }
      setIsListening(false)
      return
    }

    try {
      const recognition = new SpeechRecognitionCtor()
      ;(window as any).__weather_gpt_recognition = recognition
      recognition.lang = getLanguageMeta(language).voice
      recognition.continuous = false
      recognition.interimResults = false
      recognition.maxAlternatives = 1

      recognition.onstart = () => setIsListening(true)
      recognition.onend = () => setIsListening(false)
      recognition.onerror = (event: any) => {
        setIsListening(false)
        const errorMessage = event?.error === 'not-allowed'
          ? 'Microphone permission was denied. Please allow microphone access and try again.'
          : 'Voice capture failed. Please try again or type your question.'
        setChatAnswer(errorMessage)
      }
      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0]?.transcript || '')
          .join(' ')
          .trim()

        if (transcript) {
          setChatInput(transcript)
          setChatAnswer('Listening complete. Processing your weather question...')
          setTimeout(() => {
            void handleAskWeatherGPT()
          }, 250)
        }
      }

      recognition.start()
    } catch (error) {
      setChatAnswer('Microphone could not start. Please ensure browser permission is allowed and try again.')
    }
  }

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const freshCity = 'Current location'
          setCity(freshCity)
          const locationText = `${position.coords.latitude},${position.coords.longitude}`
          setChatInput(`Will it rain today near ${locationText}?`)
          try {
            const weatherRes = await axios.get(`${API_BASE}/weather/current`, {
              params: { latitude: position.coords.latitude, longitude: position.coords.longitude },
            })
            const forecastRes = await axios.get(`${API_BASE}/forecast`, {
              params: { latitude: position.coords.latitude, longitude: position.coords.longitude },
            })
            if (weatherRes.data?.location?.name) {
              setCity(weatherRes.data.location.name)
            }
            setWeather(weatherRes.data)
            setForecast(forecastRes.data)
          } catch (error) {
            console.error('Live location fetch error:', error)
            setCity('Chennai')
            void fetchWeatherData('Chennai')
          }
        },
        () => {
          setCity('Chennai')
          void fetchWeatherData('Chennai')
        },
        { enableHighAccuracy: true, timeout: 15000 },
      )
    } else {
      setCity('Chennai')
      void fetchWeatherData('Chennai')
    }
  }, [])

  const summaryStats = useMemo(
    () => [
      { label: 'Feels like', value: `${weather.temperature.feels_like}${weather.temperature.unit}` },
      { label: 'Humidity', value: `${weather.humidity.value}${weather.humidity.unit}` },
      { label: 'Wind', value: `${weather.wind.speed}${weather.wind.unit}` },
      { label: 'Rain', value: `${weather.precipitation.current}${weather.precipitation.unit}` },
    ],
    [weather],
  )

  return (
    <div className="weather-app-shell">
      <header className="topbar">
        <div className="brand-wrap">
          <div className="brand-mark">W</div>
          <div>
            <div className="brand-name">WeatherGPT</div>
            <div className="brand-subtitle">AI weather intelligence</div>
          </div>
        </div>

        <div className="search-bar">
          <Search size={16} />
          <input
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Search city, district, or location"
            aria-label="Search city"
          />
          <button onClick={handleSearch} className="primary-btn">
            Search
          </button>
        </div>

        <div className="topbar-actions">
          <select
            className="language-select"
            aria-label="Select language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {languageOptions.map((option) => (
              <option key={option.code} value={option.code}>
                {option.label}
              </option>
            ))}
          </select>
          <button
            className={`icon-button voice-button ${isListening ? 'active' : ''}`}
            aria-label="Voice assistant"
            onClick={handleVoiceInputToggle}
            title={isListening ? 'Stop listening' : 'Speak your weather question'}
          >
            <Mic size={18} />
          </button>
          <button
            className={`icon-button ${isSpeaking ? 'active' : ''}`}
            aria-label="Listen to answer"
            onClick={() => (isSpeaking ? stopSpeaking() : speakAnswer(chatAnswer))}
            title={isSpeaking ? 'Stop voice output' : 'Read answer aloud'}
          >
            <Volume2 size={18} />
          </button>
          <button className="icon-button" aria-label="Notifications">
            <Bell size={18} />
          </button>
        </div>
      </header>

      <main className="dashboard-layout">
        <section className="main-column">
          <div className="current-weather-card card-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">Current weather</div>
                <h2>{weather.location.name}</h2>
              </div>
              <div className="status-tag">{loading ? 'Updating…' : 'Live data'}</div>
            </div>

            <div className="temperature-row">
              <div className="temp-block">
                <div className="temp-value">{weather.temperature.current.toFixed(1)}°</div>
                <div className="condition-row">
                  {getConditionIcon(weather.condition)}
                  <span>{weather.condition}</span>
                </div>
              </div>

              <div className="metrics-grid">
                {summaryStats.map((item) => (
                  <div key={item.label} className="mini-stat">
                    <label>{item.label}</label>
                    <strong>{item.value}</strong>
                  </div>
                ))}
              </div>
            </div>

            <div className="weather-grid">
              <div className="metric-card"><Thermometer size={18} /><span>Temperature</span><strong>{weather.temperature.current.toFixed(1)}°C</strong></div>
              <div className="metric-card"><Droplets size={18} /><span>Humidity</span><strong>{weather.humidity.value}%</strong></div>
              <div className="metric-card"><Wind size={18} /><span>Wind</span><strong>{weather.wind.speed} km/h</strong></div>
              <div className="metric-card"><Gauge size={18} /><span>Pressure</span><strong>{weather.pressure.value} hPa</strong></div>
            </div>
          </div>

          <div className="forecast-card card-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">Hourly forecast</div>
                <h3>Next 24 hours</h3>
              </div>
              <button className="ghost-btn">View full forecast</button>
            </div>

            <div className="forecast-strip">
              {forecast.hourly.slice(0, 6).map((item) => (
                <div key={item.time} className="hour-card">
                  <span>{item.time}</span>
                  {getConditionIcon(item.condition)}
                  <strong>{item.temperature.toFixed(0)}°</strong>
                  <small>{item.rain_probability}% rain</small>
                </div>
              ))}
            </div>
          </div>

          <div className="daily-card card-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">7-day outlook</div>
                <h3>Weather trend</h3>
              </div>
              <button className="ghost-btn">Climate insights</button>
            </div>

            <div className="daily-table">
              {forecast.daily.map((day) => (
                <div key={day.date} className="day-row">
                  <div className="day-name">{day.date}</div>
                  <div className="day-condition">{day.condition}</div>
                  <div className="day-temp">{day.temp_max.toFixed(0)}° / {day.temp_min.toFixed(0)}°</div>
                  <div className="day-rain">{day.rain_probability}%</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <aside className="right-column">
          <div className="chat-card card-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">WeatherGPT chat</div>
                <h3>Ask about the weather</h3>
              </div>
              <div className="chat-badge">
                <MessageSquareText size={16} />
                AI
              </div>
            </div>

            <div className="chat-box">
              <div className="chat-message bot">{chatAnswer}</div>
            </div>

            <div className="prompt-row">
              {quickPrompts.map((prompt) => (
                <button key={prompt} className="prompt-pill" onClick={() => setChatInput(prompt)}>
                  {prompt}
                </button>
              ))}
            </div>

            <div className="chat-input-row">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    void handleAskWeatherGPT()
                  }
                }}
                placeholder="Ask WeatherGPT in your language..."
              />
              <button onClick={() => void handleAskWeatherGPT()} className="primary-btn small">Send</button>
            </div>
          </div>

          <div className="map-card card-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">Weather map</div>
                <h3>Location view</h3>
              </div>
              <div className="map-badge"><LocateFixed size={15} /> Live</div>
            </div>

            <div className="map-wrap">
              <MapContainer center={[weather.location.latitude, weather.location.longitude]} zoom={7} scrollWheelZoom className="leaflet-map">
                <TileLayer
                  attribution='&copy; OpenStreetMap contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[weather.location.latitude, weather.location.longitude]}>
                  <Popup>
                    <strong>{weather.location.name}</strong><br />
                    {weather.condition}<br />
                    {weather.temperature.current.toFixed(1)}°C
                  </Popup>
                </Marker>
              </MapContainer>
            </div>
          </div>

          <div className="alert-card card-panel warning-panel">
            <div className="card-header-row">
              <div>
                <div className="eyebrow">Alert feed</div>
                <h3>Extreme weather</h3>
              </div>
              <ShieldAlert size={18} />
            </div>
            <div className="alert-line">
              <strong>Moderate rainfall risk</strong>
              <span>Tonight • Chennai</span>
            </div>
            <div className="alert-line muted">
              <strong>Heat stress watch</strong>
              <span>Tomorrow • Coastal Tamil Nadu</span>
            </div>
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App
