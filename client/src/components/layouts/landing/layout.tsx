import {Outlet, useNavigate} from "react-router-dom";
import {PropsWithChildren, useEffect} from "react";

export default function LandingLayout({ children }: PropsWithChildren) {
  const pathname = useNavigate()

  useEffect(() => {
    window.scroll(0, 0)
  }, [pathname])

  return (
    <div>
      {children}
    </div>
  )
}