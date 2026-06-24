export function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600">
      <header className="p-8">
        <h1 className="text-5xl font-bold text-white">Welcome to Our Platform</h1>
        <p className="text-xl text-white/90">The best solution for everything</p>
      </header>

      <section className="py-16 px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-semibold text-white mb-8">Our Services</h2>
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <span className="text-4xl">🚀</span>
              <h3 className="text-xl font-medium text-white mt-4">Fast Performance</h3>
              <p className="text-white/80">10x faster than competitors</p>
            </div>
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <span className="text-4xl">💎</span>
              <h3 className="text-xl font-medium text-white mt-4">Premium Quality</h3>
              <p className="text-white/80">99% customer satisfaction</p>
            </div>
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <span className="text-4xl">🔒</span>
              <h3 className="text-xl font-medium text-white mt-4">Secure</h3>
              <p className="text-white/80">Enterprise-grade security</p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-semibold text-white mb-8">Why Choose Us</h2>
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <h3 className="text-xl font-medium text-white">Feature One</h3>
              <p className="text-white/80">Lorem ipsum dolor sit amet</p>
            </div>
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <h3 className="text-xl font-medium text-white">Feature Two</h3>
              <p className="text-white/80">Lorem ipsum dolor sit amet</p>
            </div>
            <div className="bg-white/10 backdrop-blur p-6 rounded-xl">
              <h3 className="text-xl font-medium text-white">Feature Three</h3>
              <p className="text-white/80">Lorem ipsum dolor sit amet</p>
            </div>
          </div>
        </div>
      </section>

      <footer className="p-8 bg-black/20">
        <p className="text-white/60">localhost:3000 - Development Mode</p>
      </footer>
    </div>
  );
}
