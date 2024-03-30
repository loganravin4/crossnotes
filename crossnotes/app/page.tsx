const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="grid grid-cols-3 items-center p-4 bg-blue-500 text-white w-full fixed top-0">
        <div className="flex gap-4 justify-start">
          <button className="bg-green-500 px-4 py-2 rounded-none">Home</button>
          <button className="bg-green-500 px-4 py-2 rounded-none">About Us</button>
          <select className="bg-green-500 px-4 py-2 rounded-none text-white text-center">
            <option>Select</option>
            <option>Student Mode</option>
            <option>Educator Mode</option>
          </select>
        </div>
        <h1 className="text-2xl text-center">Crossnotes</h1>
        <div className="flex gap-4 justify-end">
          <button className="bg-green-500 px-4 py-2 rounded-full">Login</button>
          <button className="bg-green-500 px-4 py-2 rounded-full">Sign Up</button>
        </div>
      </div>
      <div className="mt-20 text-center items-center">
        <h2 className="text-2xl">Welcome to Crossnotes!</h2>
        <p>Select an option below to start your journey!</p>
        <div className="flex gap-4 mt-4">
          <button className="bg-green-500 px-4 py-2 rounded-full">Student Mode</button>
          <button className="bg-green-500 px-4 py-2 rounded-full">Educator Mode</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
