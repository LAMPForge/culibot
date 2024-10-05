import LandingLayout from "../../components/layouts/landing/layout.tsx";
import {useNavigate} from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <LandingLayout>
      <div>
        <h1>Landing Page</h1>
        <button onClick={() => navigate('/login')}>Go to Login</button>
      </div>
    </LandingLayout>
  )
}