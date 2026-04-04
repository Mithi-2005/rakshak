import "./globals.css";

export const metadata = {
  title: "Rakshak",
  description: "AI-powered parametric insurance for gig workers",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
