'use client';

import { useCallback, useEffect, useState, type FormEvent } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

interface KiteWeatherData {
  is_kite_weather: boolean;
  verdict: string;
  wind_speed_kmh: number;
  conditions: { min_wind_kmh: number; max_wind_kmh: number };
  location: { lat: number; lon: number };
}

export default function KiteViewer() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [result, setResult] = useState<KiteWeatherData | null>(null);
  const [needleAngle, setNeedleAngle] = useState(0);
  const [animated, setAnimated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const animateTo = useCallback((angle: number) => {
    setAnimated(false);
    setNeedleAngle(0);
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        setAnimated(true);
        setNeedleAngle(angle);
      })
    );
  }, []);

  const check = useCallback(async (latitude: number, longitude: number) => {
    setError('');
    setStatus('');
    setResult(null);
    setLoading(true);
    setAnimated(false);
    setNeedleAngle(0);

    try {
      const res = await fetch(`/kite-weather?lat=${latitude}&lon=${longitude}`);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail ?? `Error ${res.status}`);
      }
      const data: KiteWeatherData = await res.json();
      setResult(data);
      animateTo(data.is_kite_weather ? 90 : -90);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  }, [animateTo]);

  const handleHere = useCallback(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser.');
      return;
    }
    setError('');
    setStatus('Getting your location…');
    setLoading(true);

    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        const la = parseFloat(coords.latitude.toFixed(5));
        const lo = parseFloat(coords.longitude.toFixed(5));
        setLat(String(la));
        setLon(String(lo));
        setStatus('');
        router.replace(`/?lat=${la}&lon=${lo}`);
        check(la, lo);
      },
      (err) => {
        setStatus('');
        setError(`Location error: ${err.message}`);
        setLoading(false);
      },
      { timeout: 10000 }
    );
  }, [check, router]);

  useEffect(() => {
    const urlLat = searchParams.get('lat');
    const urlLon = searchParams.get('lon');
    const here = searchParams.get('here');

    if (urlLat && urlLon) {
      setLat(urlLat);
      setLon(urlLon);
      check(parseFloat(urlLat), parseFloat(urlLon));
    } else if (here !== null) {
      handleHere();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const la = parseFloat(lat);
    const lo = parseFloat(lon);
    router.replace(`/?lat=${la}&lon=${lo}`);
    check(la, lo);
  }

  const arcRedOpacity = result && !result.is_kite_weather ? 0.9 : 0.25;
  const arcGreenOpacity = result?.is_kite_weather ? 0.9 : 0.25;
  const arcRedFilter = result && !result.is_kite_weather ? 'url(#glow-red)' : undefined;
  const arcGreenFilter = result?.is_kite_weather ? 'url(#glow-green)' : undefined;
  const verdictColor = result ? (result.is_kite_weather ? '#22c55e' : '#ef4444') : 'transparent';

  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-8 p-8">

      <h1 className="text-xl font-semibold tracking-[0.08em] text-slate-400 uppercase">
        Kite Weather
      </h1>

      {/* ── Gauge ── */}
      <div className="w-80 h-[210px]">
        <svg viewBox="0 0 320 210" width="320" height="210" style={{ overflow: 'visible' }}>
          <defs>
            <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
          </defs>

          {/* Dim track */}
          <path d="M 35 185 A 125 125 0 0 1 160 60 A 125 125 0 0 1 285 185"
            fill="none" stroke="#1e2a3a" strokeWidth="20" strokeLinecap="round" />

          {/* Red zone: 9:00 → 12:00 */}
          <path d="M 35 185 A 125 125 0 0 1 160 60"
            fill="none" stroke="#ef4444" strokeWidth="20" strokeLinecap="round"
            opacity={arcRedOpacity} filter={arcRedFilter}
            style={{ transition: 'opacity 0.4s' }}
          />

          {/* Green zone: 12:00 → 3:00 */}
          <path d="M 160 60 A 125 125 0 0 1 285 185"
            fill="none" stroke="#22c55e" strokeWidth="20" strokeLinecap="round"
            opacity={arcGreenOpacity} filter={arcGreenFilter}
            style={{ transition: 'opacity 0.4s' }}
          />

          {/* 12:00 tick */}
          <line x1="160" y1="58" x2="160" y2="74" stroke="#334155" strokeWidth="2" strokeLinecap="round" />

          {/* Needle */}
          <g style={{
            transformBox: 'view-box',
            transformOrigin: '160px 185px',
            transform: `rotate(${needleAngle}deg)`,
            transition: animated ? 'transform 1.4s cubic-bezier(0.34, 1.4, 0.64, 1)' : 'none',
          }}>
            <line x1="160" y1="185" x2="160" y2="75" stroke="#000" strokeWidth="5" strokeLinecap="round" opacity="0.3" />
            <line x1="160" y1="185" x2="160" y2="75" stroke="#e2e8f0" strokeWidth="3" strokeLinecap="round" />
            <circle cx="160" cy="185" r="9" fill="#1e2a3a" stroke="#e2e8f0" strokeWidth="2" />
            <circle cx="160" cy="185" r="4" fill="#e2e8f0" />
          </g>
        </svg>
      </div>

      <p className="text-2xl font-bold min-h-8 text-center tracking-wide transition-colors duration-300"
        style={{ color: verdictColor }}>
        {result?.verdict ?? '—'}
      </p>

      <p className="text-sm text-slate-600 text-center min-h-5">
        {status || (result
          ? `Wind: ${result.wind_speed_kmh} km/h · Kite range: ${result.conditions.min_wind_kmh}–${result.conditions.max_wind_kmh} km/h`
          : '')}
      </p>

      <form className="flex gap-2 flex-wrap justify-center" onSubmit={handleSubmit}>
        <input
          className="bg-[#161b27] border border-[#2d3748] text-slate-200 px-3 py-2 rounded-lg text-sm w-[130px] outline-none appearance-none focus:border-[#4f8ef7] placeholder:text-slate-700 transition-colors"
          type="number" placeholder="Latitude"
          value={lat} onChange={e => setLat(e.target.value)}
          step="any" min="-90" max="90" required
        />
        <input
          className="bg-[#161b27] border border-[#2d3748] text-slate-200 px-3 py-2 rounded-lg text-sm w-[130px] outline-none appearance-none focus:border-[#4f8ef7] placeholder:text-slate-700 transition-colors"
          type="number" placeholder="Longitude"
          value={lon} onChange={e => setLon(e.target.value)}
          step="any" min="-180" max="180" required
        />
        <button
          className="bg-[#4f8ef7] text-white px-5 py-2 rounded-lg text-sm font-semibold cursor-pointer hover:bg-[#3b7de8] disabled:bg-slate-700 disabled:cursor-default transition-colors"
          type="submit" disabled={loading}
        >
          Check
        </button>
        <button
          className="bg-transparent border border-[#2d3748] text-slate-500 text-sm px-4 py-2 rounded-lg cursor-pointer hover:border-[#4f8ef7] hover:text-slate-200 disabled:border-[#1e293b] disabled:text-slate-700 transition-colors"
          type="button" disabled={loading} onClick={handleHere}
        >
          ⊙ Here
        </button>
      </form>

      <p className="text-red-400 text-xs min-h-4 text-center">{error}</p>

    </main>
  );
}
