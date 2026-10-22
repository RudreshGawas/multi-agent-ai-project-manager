import "./globals.css";

export const metadata = {
  title: "Project Pilot | AI Project Manager",
  description: "Turn a project idea into a structured software delivery plan.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
